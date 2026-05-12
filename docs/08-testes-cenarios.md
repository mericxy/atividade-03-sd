# Testes e Cenários

## Objetivo dos Cenários

Os cenários devem demonstrar como a conectividade influencia entrega, latência e overhead.

A atividade exige pelo menos:

- cenário denso;
- cenário esparso;
- cenário com mobilidade em cadeia.

Os arquivos prontos estão em [cenarios/](cenarios/).

## Cenário Denso

Arquivo:

```text
docs/cenarios/denso/contacts.txt
docs/cenarios/denso/messages.txt
```

Características:

- muitos contatos;
- vários caminhos alternativos;
- maior replicação de mensagens;
- tendência a alta taxa de entrega;
- tendência a overhead elevado.

Hipótese esperada:

```text
taxa_entrega alta
latencia_media baixa ou média
overhead alto
```

## Cenário Esparso

Arquivo:

```text
docs/cenarios/esparso/contacts.txt
docs/cenarios/esparso/messages.txt
```

Características:

- poucos contatos;
- longos intervalos sem conexão;
- alguns destinos podem nunca ser alcançados;
- tendência a menor taxa de entrega;
- latência maior nas mensagens entregues.

Hipótese esperada:

```text
taxa_entrega baixa ou média
latencia_media alta
overhead baixo ou médio
```

## Cenário Cadeia

Arquivo:

```text
docs/cenarios/cadeia/contacts.txt
docs/cenarios/cadeia/messages.txt
```

Características:

- nós conectam em sequência;
- exemplo clássico de store-and-forward;
- mensagem precisa passar por intermediários;
- bom para verificar TTL e caminho.

Hipótese esperada:

```text
mensagem 1 -> 4 entregue se houver contatos 1-2, 2-3 e 3-4 nessa ordem
latencia depende do tempo entre os contatos
overhead moderado
```

## Testes Unitários Recomendados

### Parser de Contatos

Validar:

- leitura de linhas válidas;
- ignorar comentários;
- rejeitar campos faltantes;
- rejeitar `tempo_fim < tempo_inicio`;
- ordenar por tempo.

### Parser de Mensagens

Validar:

- criação de mensagens com TTL;
- geração de IDs;
- payload com espaços;
- rejeição de TTL negativo.

### Buffer do Nó

Validar:

- inserção de mensagem;
- não duplicar mensagem já vista;
- manter `seen_messages`;
- persistir e recarregar buffer, se houver JSON.

### Roteamento Epidêmico

Validar:

- troca de resumos;
- envio apenas de mensagens ausentes;
- decremento de TTL;
- entrega quando receptor é destino;
- não envio quando TTL é zero.

### Métricas

Validar:

- taxa de entrega;
- latência média;
- overhead;
- não contar entrega duplicada.

## Testes de Integração

Rodar cada cenário completo:

```bash
python dtp2p.py simulate --contacts docs/cenarios/denso/contacts.txt --messages docs/cenarios/denso/messages.txt
python dtp2p.py simulate --contacts docs/cenarios/esparso/contacts.txt --messages docs/cenarios/esparso/messages.txt
python dtp2p.py simulate --contacts docs/cenarios/cadeia/contacts.txt --messages docs/cenarios/cadeia/messages.txt
```

## Critérios de Aceitação

A entrega é considerada completa quando:

- os três cenários executam sem erro;
- o relatório final é gerado;
- a taxa de entrega é calculada corretamente;
- a latência média é calculada apenas para mensagens entregues;
- o overhead considera todas as transmissões;
- mensagens não são encaminhadas com TTL zero;
- loops são evitados por `seen_messages`;
- o log mostra contatos e transmissões relevantes.

