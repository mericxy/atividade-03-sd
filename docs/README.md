# Documentação da Atividade DTN P2P

Esta pasta descreve a arquitetura proposta para a atividade prática de Sistemas Distribuídos: uma rede P2P simulada para DTN, com comunicação intermitente, armazenamento local e roteamento epidêmico.

## Como Ler Esta Documentação

1. Comece por [01-visao-geral.md](01-visao-geral.md) para entender o escopo da atividade.
2. Leia [02-arquitetura-geral.md](02-arquitetura-geral.md) para conhecer os módulos do sistema.
3. Use [03-modelo-de-dados.md](03-modelo-de-dados.md) e [04-protocolo-p2p-epidemico.md](04-protocolo-p2p-epidemico.md) como referência de implementação.
4. Consulte [05-simulacao-eventos.md](05-simulacao-eventos.md) para montar o motor de simulação.
5. Valide a entrega com [06-metricas-relatorio.md](06-metricas-relatorio.md) e [08-testes-cenarios.md](08-testes-cenarios.md).

## Estrutura dos Arquivos

```text
docs/
├── README.md
├── 01-visao-geral.md
├── 02-arquitetura-geral.md
├── 03-modelo-de-dados.md
├── 04-protocolo-p2p-epidemico.md
├── 05-simulacao-eventos.md
├── 06-metricas-relatorio.md
├── 07-interface-execucao.md
├── 08-testes-cenarios.md
├── 09-extensao-prophet.md
├── 10-plano-implementacao.md
├── diagramas.md
└── cenarios/
    ├── README.md
    ├── denso/
    │   ├── contacts.txt
    │   └── messages.txt
    ├── esparso/
    │   ├── contacts.txt
    │   └── messages.txt
    └── cadeia/
        ├── contacts.txt
        └── messages.txt
```

## Decisão Principal da Arquitetura

A implementação recomendada é uma simulação baseada em eventos discretos em um único processo. Cada nó P2P é representado como uma entidade independente dentro da simulação, com seu próprio buffer, lista de mensagens vistas, relógio lógico e regras de troca.

Essa abordagem atende aos requisitos da atividade sem exigir sincronização real entre processos, portas locais ou threads. Caso a disciplina exija processos reais, a mesma arquitetura pode ser adaptada para sockets TCP/UDP, mantendo os mesmos módulos conceituais.

## Resultado Esperado

Ao final, o projeto deve permitir:

- carregar uma lista de contatos intermitentes;
- carregar mensagens iniciais;
- simular encontros P2P sem servidor central;
- encaminhar mensagens por roteamento epidêmico;
- comparar o roteamento epidêmico com a extensão PROPHET;
- respeitar TTL por mensagem;
- evitar loops por IDs de mensagens vistas;
- gerar relatório com taxa de entrega, latência média e overhead;
- executar pelo menos três cenários: denso, esparso e cadeia.
