# Simulação Baseada em Eventos

## Motivação

A simulação por eventos discretos permite reproduzir os mesmos resultados em qualquer execução. Em vez de usar tempo real, o simulador processa eventos em ordem crescente de tempo.

Isso é ideal para DTN porque os contatos são conhecidos previamente pelo arquivo `contacts.txt`.

## Tipos de Evento

| Evento | Origem | Descrição |
|---|---|---|
| `MESSAGE_INJECTION` | `messages.txt` ou CLI | Cria uma mensagem no buffer do nó de origem. |
| `CONTACT_START` | `contacts.txt` | Dispara uma troca P2P entre dois nós. |
| `REPORT` | Simulador | Gera métricas finais. |

Na versão mínima, `CONTACT_END` não precisa ser processado se toda troca for considerada instantânea no início do contato.

## Modelo de Tempo

O tempo é um `float` em segundos simulados.

Exemplo:

```text
t=0.0  mensagem m-1-0001 criada no nó 1
t=1.0  contato 1 <-> 2
t=3.5  contato 2 <-> 4
t=3.5  m-1-0001 entregue ao nó 4
```

## Fila de Eventos

A fila deve ordenar eventos por:

1. tempo;
2. prioridade;
3. ordem de inserção.

Prioridade recomendada quando eventos têm o mesmo tempo:

| Prioridade | Evento |
|---|---|
| 1 | `MESSAGE_INJECTION` |
| 2 | `CONTACT_START` |
| 3 | `REPORT` |

Isso garante que uma mensagem criada no mesmo instante de um contato já esteja disponível para transmissão.

## Algoritmo do Motor

```text
load_config()
load_contacts()
load_messages()
create_nodes()
schedule_events()

while event_queue is not empty:
    event = event_queue.pop()
    current_time = event.time

    if event.type == MESSAGE_INJECTION:
        inject_message(event)

    if event.type == CONTACT_START:
        run_contact(event.node_a, event.node_b, current_time)

generate_report()
```

## Criação de Nós

O simulador deve criar nós automaticamente a partir:

- dos IDs presentes em `contacts.txt`;
- das origens e destinos presentes em `messages.txt`;
- de uma lista explícita passada por CLI, se existir.

## Duração do Contato

Para a versão mínima, a duração do contato pode ser usada apenas para registro. Toda troca ocorre em `tempo_inicio`.

Para uma versão mais realista, a duração pode limitar a quantidade de mensagens transmitidas:

```text
capacidade_do_contato = largura_banda * (tempo_fim - tempo_inicio)
```

Essa extensão não é necessária para cumprir os requisitos mínimos.

## Controlador de Contatos

Responsabilidades:

- abrir arquivo de contatos;
- ignorar linhas vazias;
- permitir comentários iniciados por `#`;
- validar número de campos;
- converter tempos para `float`;
- converter IDs para `int`;
- ordenar contatos por `tempo_inicio`;
- expor lista de `ContactEvent`.

## Exemplo de Entrada

```text
# tempo_inicio, tempo_fim, noA, noB
0.0, 5.0, 1, 2
5.1, 8.0, 2, 3
8.2, 12.0, 3, 1
```

## Exemplo de Log

```text
[sim] t=0.0 mensagem m-1-0001 criada em 1 para 4
[1] contato com 2 em t=0.0
[1] enviando m-1-0001 para 2 ttl=4
[2] recebeu m-1-0001 ttl=3
[2] contato com 3 em t=5.1
[2] enviando m-1-0001 para 3 ttl=3
[3] recebeu m-1-0001 ttl=2
```

## Modo com Threads ou Sockets

Caso a implementação use processos reais:

- cada nó executa um processo;
- o controlador de contatos envia sinais para liberar comunicação entre pares;
- cada nó mantém seu próprio buffer em arquivo;
- a troca epidêmica acontece por TCP ou UDP;
- o relatório precisa agregar logs ao final.

Essa alternativa é mais complexa. A simulação por eventos é recomendada para a entrega mínima.

