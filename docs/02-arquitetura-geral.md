# Arquitetura Geral

## Estilo Arquitetural

A arquitetura é modular e orientada a simulação. O sistema não possui servidor central; todos os nós são pares independentes dentro do motor de simulação.

Na versão mínima, os nós não precisam ser processos reais. Cada nó pode ser um objeto com estado próprio. A ausência de servidor central é preservada porque nenhuma entidade global decide o conteúdo das trocas P2P; o simulador apenas agenda contatos e avança o tempo.

## Componentes

| Componente | Responsabilidade |
|---|---|
| `SimulationEngine` | Carrega entradas, ordena eventos, avança tempo e coordena contatos. |
| `ContactController` | Lê `contacts.txt` e cria eventos de contato. |
| `MessageLoader` | Lê mensagens iniciais ou comandos de envio. |
| `Node` | Representa um nó P2P com buffer, mensagens vistas e relógio lógico. |
| `MessageBuffer` | Armazena mensagens de forma persistente ou simulada. |
| `EpidemicRouter` | Executa troca de resumos e transferência de mensagens ausentes. |
| `MetricsCollector` | Registra transmissões, entregas, latências e resultados finais. |
| `ReportWriter` | Exporta relatório em texto, JSON ou CSV. |
| `CLI` | Expõe comandos para executar simulações e enviar mensagens. |

## Estrutura Sugerida de Código

```text
atividade-03-sd/
├── dtp2p.py
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── event.py
│   │   └── clock.py
│   ├── contacts/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   └── parser.py
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── node.py
│   │   └── buffer.py
│   ├── routing/
│   │   ├── __init__.py
│   │   ├── epidemic.py
│   │   └── prophet.py
│   ├── messages/
│   │   ├── __init__.py
│   │   ├── message.py
│   │   └── parser.py
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── collector.py
│   │   └── report.py
│   └── persistence/
│       ├── __init__.py
│       └── json_store.py
├── tests/
│   ├── test_contacts.py
│   ├── test_epidemic.py
│   ├── test_metrics.py
│   └── test_scenarios.py
└── docs/
```

## Fluxo de Execução

1. CLI recebe caminhos de `contacts.txt` e `messages.txt`.
2. `ContactController` carrega contatos e valida intervalos.
3. `MessageLoader` carrega mensagens iniciais.
4. `SimulationEngine` cria nós envolvidos nos contatos e mensagens.
5. Cada mensagem inicial é inserida no buffer do nó de origem.
6. Eventos de contato são processados em ordem de `tempo_inicio`.
7. Em cada contato, `EpidemicRouter` troca resumos entre os dois nós.
8. Cada nó envia ao outro as mensagens que o outro ainda não viu e cujo TTL permite repasse.
9. `MetricsCollector` registra cada transmissão e cada entrega única.
10. Ao final, `ReportWriter` gera relatório com métricas.

## Separação de Responsabilidades

O simulador não deve saber como o roteamento escolhe mensagens. Ele apenas informa que dois nós estão em contato.

O roteador não deve saber como relatórios são escritos. Ele apenas executa trocas e notifica métricas.

O nó não deve calcular métricas globais. Ele apenas mantém seu estado local.

O coletor de métricas não deve alterar buffers. Ele apenas observa eventos relevantes.

## Estado Global Permitido

O único estado global recomendado é o estado da simulação: tempo atual, fila de eventos, conjunto de nós e métricas agregadas. Esse estado pertence ao `SimulationEngine`.

Essa centralização não viola a lógica P2P da atividade, pois ela representa o ambiente de simulação, não um servidor de rede usado pelos nós para entregar mensagens.

## Persistência

Para a versão mínima, o buffer pode existir em memória durante uma simulação.

Para evidenciar a ideia de fila persistente, recomenda-se implementar uma camada opcional de persistência em JSON:

```text
data/
└── nodes/
    ├── node-1-buffer.json
    ├── node-2-buffer.json
    └── node-3-buffer.json
```

Cada arquivo pode guardar as mensagens armazenadas por um nó. Isso permite reiniciar uma simulação ou inspecionar manualmente o estado.

