# Métricas e Relatório

## Métricas Obrigatórias

### Taxa de Entrega

```text
taxa_entrega = mensagens_entregues_unicas / total_mensagens_criadas
```

Exemplo:

```text
8 mensagens entregues / 10 mensagens criadas = 0.80
```

### Latência Média

```text
latencia_media = soma(latencia_das_mensagens_entregues) / mensagens_entregues_unicas
```

Para cada mensagem entregue:

```text
latencia = delivered_at - created_at
```

Mensagens não entregues não entram na latência média.

### Overhead

```text
overhead = total_transmissoes / mensagens_entregues_unicas
```

Uma transmissão é qualquer envio de cópia entre dois nós, mesmo que não resulte em entrega.

Se nenhuma mensagem for entregue:

```text
overhead = total_transmissoes
```

ou

```text
overhead = null
```

A documentação do relatório deve deixar claro qual escolha foi usada. Recomendação: usar `null` para evitar divisão por zero.

## Contadores

| Contador | Descrição |
|---|---|
| `total_created` | Total de mensagens criadas. |
| `unique_deliveries` | Total de mensagens entregues pela primeira vez ao destino. |
| `total_transmissions` | Total de cópias transmitidas entre pares. |
| `duplicate_deliveries` | Mensagens recebidas pelo destino depois da primeira entrega. |
| `expired_messages` | Mensagens que chegaram a TTL zero. |
| `contacts_processed` | Quantidade de contatos processados. |

## Relatório em Texto

Exemplo:

```text
Relatório da Simulação DTN P2P
==============================

Cenário: cadeia
Nós: 4
Mensagens criadas: 3
Contatos processados: 6

Entregas únicas: 2
Taxa de entrega: 66.67%
Latência média: 7.40s
Transmissões totais: 8
Overhead: 4.00

Mensagens:
- m-1-0001: entregue em t=8.0, latência=8.0s, caminho=1->2->3->4
- m-4-0001: entregue em t=6.8, latência=6.3s, caminho=4->3->2->1
- m-2-0001: não entregue
```

## Relatório em JSON

Formato recomendado:

```json
{
  "scenario": "cadeia",
  "nodes": 4,
  "total_created": 3,
  "unique_deliveries": 2,
  "delivery_rate": 0.6667,
  "average_latency": 7.4,
  "total_transmissions": 8,
  "overhead": 4.0,
  "contacts_processed": 6,
  "messages": [
    {
      "id": "m-1-0001",
      "source_id": 1,
      "destination_id": 4,
      "status": "delivered",
      "created_at": 0.0,
      "delivered_at": 8.0,
      "latency": 8.0,
      "path": [1, 2, 3, 4]
    }
  ]
}
```

## Arquivos de Saída

Sugestão:

```text
reports/
├── denso-report.txt
├── denso-report.json
├── esparso-report.txt
├── esparso-report.json
├── cadeia-report.txt
└── cadeia-report.json
```

## Interpretação Esperada

| Cenário | Taxa de entrega | Latência | Overhead |
|---|---|---|---|
| Denso | Alta | Baixa a média | Alto |
| Esparso | Baixa a média | Alta | Baixo a médio |
| Cadeia | Depende da ordem dos contatos | Média a alta | Controlado |

## Cuidados na Avaliação

- Uma taxa de entrega alta pode vir acompanhada de overhead alto.
- Uma rede muito esparsa pode ter overhead baixo simplesmente porque quase nada é transmitido.
- Latência média só considera mensagens entregues; por isso deve ser lida junto com taxa de entrega.
- TTL baixo reduz overhead, mas pode impedir entregas.
- TTL alto aumenta chance de entrega, mas aumenta replicação.

