# Extensão: Roteamento PROPHET

## Objetivo

PROPHET é uma alternativa ao roteamento epidêmico. Em vez de replicar mensagens para todos os nós que ainda não as possuem, ele usa probabilidades de entrega baseadas no histórico de encontros.

A extensão permite comparar:

- entrega;
- latência;
- overhead;
- custo de replicação.

## Ideia Geral

Cada nó mantém uma probabilidade de entrega para cada destino:

```text
P(a, b) = probabilidade de o nó A entregar uma mensagem ao nó B
```

Quando dois nós se encontram, eles atualizam suas probabilidades.

## Regras Principais

### Atualização por Encontro

Quando `A` encontra `B`, a probabilidade de `A` entregar para `B` aumenta:

```text
P(a,b) = P(a,b)_old + (1 - P(a,b)_old) * P_INIT
```

Valor comum:

```text
P_INIT = 0.75
```

### Envelhecimento

Com o tempo, probabilidades diminuem:

```text
P(a,b) = P(a,b)_old * GAMMA^k
```

Valor comum:

```text
GAMMA = 0.98
```

`k` representa unidades de tempo desde a última atualização.

### Transitividade

Se `A` encontra `B`, e `B` tem boa probabilidade de entregar a `C`, então `A` também pode aumentar sua probabilidade para `C`:

```text
P(a,c) = P(a,c)_old + (1 - P(a,c)_old) * P(a,b) * P(b,c) * BETA
```

Valor comum:

```text
BETA = 0.25
```

## Critério de Encaminhamento

`A` envia uma mensagem com destino `D` para `B` se:

```text
P(b,d) > P(a,d)
```

e:

- `B` ainda não viu a mensagem;
- `ttl > 0`;
- o buffer de `B` aceita a mensagem.

## Mudanças na Arquitetura

Implementado em `src/routing/prophet.py`:

```text
ProphetRouter
├── delivery_probabilities
├── update_on_contact()
├── age_probabilities()
├── apply_transitivity()
└── should_forward()
```

Adicionado ao `NodeState` em `src/nodes/node.py`:

```text
delivery_probabilities: map[int, float]
last_probability_update: float
```

Adicionar parâmetro na CLI:

```bash
python dtp2p.py simulate \
  --router prophet \
  --contacts docs/cenarios/denso/contacts.txt \
  --messages docs/cenarios/denso/messages.txt
```

Também é possível salvar o relatório:

```bash
python dtp2p.py simulate \
  --router prophet \
  --contacts docs/cenarios/denso/contacts.txt \
  --messages docs/cenarios/denso/messages.txt \
  --report reports/denso-prophet-report.json
```

## Comparação com Epidêmico

| Critério | Epidêmico | PROPHET |
|---|---|---|
| Decisão | Envia para quem não tem | Envia para quem tem maior chance de entrega |
| Overhead | Alto | Menor |
| Entrega em rede densa | Alta | Alta |
| Entrega em rede esparsa | Pode ser boa com TTL alto | Depende do histórico |
| Complexidade | Baixa | Média |

## Relatório Comparativo

Sugestão de saída:

```text
Cenário: denso

Roteador    Entrega    Latência média    Transmissões    Overhead
Epidemic    100%       3.2s              42              7.0
PROPHET     83%        4.1s              18              3.6
```

## Cuidados

PROPHET depende de histórico de encontros. Em uma simulação curta, pode não haver tempo suficiente para as probabilidades se tornarem úteis.

Para uma comparação justa:

- usar os mesmos contatos;
- usar as mesmas mensagens;
- usar o mesmo TTL;
- executar cenários com contatos repetidos.
