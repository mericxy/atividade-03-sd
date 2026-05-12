# Protocolo P2P Epidêmico

## Ideia Central

No roteamento epidêmico, quando dois nós se encontram, eles comparam as mensagens que conhecem. Cada nó envia ao outro as mensagens que o outro ainda não possui, respeitando TTL.

Esse comportamento aumenta a chance de entrega em redes desconectadas, porque cria múltiplas cópias da mesma mensagem em diferentes partes da rede.

## Etapas de um Contato

Para um contato entre `A` e `B` no tempo `t`:

1. Atualizar relógio lógico de `A` e `B` para `t`.
2. `A` envia a `B` um resumo dos IDs em seu buffer.
3. `B` envia a `A` um resumo dos IDs em seu buffer.
4. `A` calcula quais mensagens possui e `B` não possui.
5. `B` calcula quais mensagens possui e `A` não possui.
6. Cada lado filtra mensagens com `ttl > 0`.
7. As transmissões são executadas.
8. O receptor adiciona o ID em `seen_messages`.
9. Se o receptor for o destino, registrar entrega única.
10. Registrar cada transmissão no coletor de métricas.

## Resumo de Mensagens

O resumo é um conjunto de IDs:

```text
summary(A) = {m-1-0001, m-2-0003, m-4-0002}
```

Na versão mínima, o resumo pode ser derivado de `buffer.keys()`.

Uma versão mais conservadora pode usar `seen_messages`, impedindo que o nó receba novamente uma mensagem que ele já descartou. Para a atividade, usar `seen_messages` é recomendado para evitar loops com mais clareza.

## Critério de Envio

O nó `A` envia a mensagem `m` para `B` se:

- `m.id` está no buffer de `A`;
- `m.id` não está em `seen_messages` de `B`;
- `m.ttl > 0`;
- `B` não é o último nó no `path` da cópia de `m`, para evitar retorno imediato;
- a política de buffer de `B` aceita a mensagem.

## TTL

O TTL representa o número de saltos restantes.

Exemplo:

```text
A possui m1 com TTL=3
A envia m1 para B
B recebe m1 com TTL=2
B envia m1 para C
C recebe m1 com TTL=1
```

Quando TTL chega a zero, a mensagem pode continuar armazenada, mas não deve ser encaminhada novamente.

## Entrega

Uma mensagem é entregue quando o nó receptor tem `node_id == destination_id`.

A primeira entrega registra:

- `message_id`;
- destino;
- tempo de entrega;
- latência;
- caminho da cópia entregue.

Entregas repetidas da mesma mensagem ao mesmo destino devem ser ignoradas para a métrica de entregas únicas, mas as transmissões ainda contam para overhead.

## Ordem das Trocas

Há duas opções aceitáveis:

### Troca Simétrica por Rodada

Os dois nós calculam os conjuntos de envio antes de qualquer transferência.

Vantagem: comportamento mais previsível.

### Troca Sequencial

`A` envia para `B`, depois `B` recalcula e envia para `A`.

Vantagem: simples, mas pode permitir que uma mensagem recebida no mesmo contato volte imediatamente, se não houver cuidado.

Recomendação: usar troca simétrica por rodada.

## Pseudocódigo

```text
on_contact(node_a, node_b, time):
    node_a.clock = time
    node_b.clock = time

    summary_a = node_a.seen_messages
    summary_b = node_b.seen_messages

    send_a_to_b = []
    send_b_to_a = []

    for message in node_a.buffer:
        if message.id not in summary_b and message.ttl > 0:
            send_a_to_b.append(message)

    for message in node_b.buffer:
        if message.id not in summary_a and message.ttl > 0:
            send_b_to_a.append(message)

    for message in send_a_to_b:
        transfer(message, node_a, node_b, time)

    for message in send_b_to_a:
        transfer(message, node_b, node_a, time)
```

## Função de Transferência

```text
transfer(message, sender, receiver, time):
    copied = copy(message)
    copied.ttl = message.ttl - 1
    copied.hop_count = message.hop_count + 1
    copied.path = message.path + [receiver.id]

    receiver.buffer[copied.id] = copied
    receiver.seen_messages.add(copied.id)

    metrics.record_transmission(time, copied.id, sender.id, receiver.id)

    if receiver.id == copied.destination_id:
        metrics.record_delivery(copied, time)
```

## Controle de Loops

O controle de loops depende de dois mecanismos:

- `seen_messages`: impede receber novamente uma mensagem já conhecida.
- `ttl`: impede que cópias circulem indefinidamente caso a política de vistos seja alterada ou falhe.

## Limitação do Roteamento Epidêmico

O roteamento epidêmico consome muitos recursos, pois replica mensagens agressivamente. Esse comportamento é útil para comparar cenários, mas aumenta overhead quando a rede é densa.

