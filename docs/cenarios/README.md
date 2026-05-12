# Cenários de Teste

Esta pasta contém entradas de exemplo para validar a simulação DTN P2P.

Cada cenário possui:

- `contacts.txt`: janelas de contato entre pares de nós;
- `messages.txt`: mensagens criadas durante a simulação.

## Formato de `contacts.txt`

```text
tempo_inicio, tempo_fim, noA, noB
```

Exemplo:

```text
0.0, 5.0, 1, 2
```

## Formato de `messages.txt`

```text
tempo, origem, destino, ttl, payload
```

Exemplo:

```text
0.0, 1, 4, 5, ola do no 1 para o no 4
```

## Cenários

| Cenário | Finalidade |
|---|---|
| `denso` | Avaliar alta conectividade e overhead. |
| `esparso` | Avaliar baixa conectividade e latência. |
| `cadeia` | Demonstrar store-and-forward por intermediários. |

