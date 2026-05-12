# Modelo de Dados

## Message

Representa uma mensagem DTN transportada pelos nós.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | Identificador único da mensagem. |
| `source_id` | int | Nó que criou a mensagem. |
| `destination_id` | int | Nó destino. |
| `payload` | string | Conteúdo da mensagem. |
| `created_at` | float | Tempo simulado de criação. |
| `ttl` | int | Número máximo de saltos restantes. |
| `hop_count` | int | Quantidade de saltos já realizados. |
| `delivered_at` | float/null | Tempo da primeira entrega ao destino. |
| `path` | list[int] | Nós pelos quais a cópia atual passou. |

Exemplo em JSON:

```json
{
  "id": "m1",
  "source_id": 1,
  "destination_id": 4,
  "payload": "ola",
  "created_at": 0.0,
  "ttl": 5,
  "hop_count": 0,
  "delivered_at": null,
  "path": [1]
}
```

## NodeState

Representa o estado local de um nó.

| Campo | Tipo | Descrição |
|---|---|---|
| `node_id` | int | Identificador do nó. |
| `clock` | float | Relógio lógico ou último tempo simulado conhecido. |
| `buffer` | map[string, Message] | Mensagens armazenadas pelo nó. |
| `seen_messages` | set[string] | IDs de mensagens já vistas pelo nó. |
| `delivered_messages` | set[string] | IDs entregues localmente, se o nó for destino. |

## ContactEvent

Representa uma janela de conectividade entre dois nós.

| Campo | Tipo | Descrição |
|---|---|---|
| `start_time` | float | Início do contato. |
| `end_time` | float | Fim do contato. |
| `node_a` | int | Primeiro nó. |
| `node_b` | int | Segundo nó. |
| `duration` | float | `end_time - start_time`. |

Formato de arquivo:

```text
tempo_inicio, tempo_fim, noA, noB
```

Exemplo:

```text
0.0, 5.0, 1, 2
5.1, 8.0, 2, 3
8.2, 12.0, 3, 1
```

## MessageInjection

Representa a criação de uma mensagem em um tempo simulado.

Formato recomendado para `messages.txt`:

```text
tempo, origem, destino, ttl, payload
```

Exemplo:

```text
0.0, 1, 4, 5, ola do no 1 para o no 4
2.0, 3, 1, 4, resposta do no 3
```

## DeliveryRecord

Representa uma entrega única.

| Campo | Tipo | Descrição |
|---|---|---|
| `message_id` | string | ID da mensagem entregue. |
| `source_id` | int | Origem. |
| `destination_id` | int | Destino. |
| `created_at` | float | Tempo de criação. |
| `delivered_at` | float | Tempo de entrega. |
| `latency` | float | `delivered_at - created_at`. |
| `first_delivery_node` | int | Nó que recebeu a mensagem como destino. |
| `path` | list[int] | Caminho da cópia entregue. |

## TransmissionRecord

Representa uma transmissão P2P entre dois nós.

| Campo | Tipo | Descrição |
|---|---|---|
| `time` | float | Tempo simulado da transmissão. |
| `message_id` | string | Mensagem transmitida. |
| `from_node` | int | Nó remetente da transmissão. |
| `to_node` | int | Nó receptor da transmissão. |
| `ttl_before` | int | TTL antes da transmissão. |
| `ttl_after` | int | TTL da cópia recebida. |
| `delivered` | bool | Indica se a transmissão resultou em entrega final. |

## Regras de Identificação

O ID da mensagem pode ser gerado como:

```text
m-{source_id}-{sequence_number}
```

Exemplo:

```text
m-1-0001
m-1-0002
m-3-0001
```

Essa regra evita colisões sem exigir serviço central.

## Regras de Cópia

Ao transmitir uma mensagem, o nó receptor recebe uma cópia independente da mensagem, com:

- `ttl` decrementado em 1;
- `hop_count` incrementado em 1;
- `path` atualizado com o ID do receptor;
- mesmo `id`, `source_id`, `destination_id`, `payload` e `created_at`.

## Validações

O sistema deve rejeitar ou reportar erro quando:

- `tempo_fim < tempo_inicio`;
- `ttl < 0`;
- origem e destino da mensagem forem iguais, se a versão mínima não tratar entrega imediata;
- contato possuir IDs de nós inválidos;
- linha de entrada estiver incompleta.

