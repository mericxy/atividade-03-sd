# Plano de Implementação

## Etapa 1: Estrutura Inicial

Criar a estrutura de diretórios:

```text
src/
tests/
reports/
data/
```

Criar o ponto de entrada:

```text
dtp2p.py
```

## Etapa 2: Modelos

Implementar:

- `Message`;
- `Node`;
- `ContactEvent`;
- `MessageInjection`;
- `TransmissionRecord`;
- `DeliveryRecord`.

Recomendação em Python:

```python
from dataclasses import dataclass
```

## Etapa 3: Parsers

Implementar:

- parser de `contacts.txt`;
- parser de `messages.txt`;
- validação de campos;
- suporte a comentários com `#`;
- mensagens de erro claras.

## Etapa 4: Buffer e Estado do Nó

Implementar:

- `buffer`;
- `seen_messages`;
- `delivered_messages`;
- inserção sem duplicidade;
- cópia de mensagem com decremento de TTL;
- persistência opcional em JSON.

## Etapa 5: Motor de Simulação

Implementar:

- fila de eventos;
- ordenação por tempo;
- injeção de mensagens;
- contatos;
- logs;
- finalização.

## Etapa 6: Roteamento Epidêmico

Implementar:

- troca de resumos;
- cálculo de mensagens ausentes;
- transferência simétrica;
- decremento de TTL;
- registro de transmissão;
- registro de entrega.

## Etapa 7: Métricas

Implementar:

- total de mensagens;
- entregas únicas;
- transmissões;
- latência por mensagem;
- latência média;
- overhead;
- relatório em texto ou JSON.

## Etapa 8: CLI

Implementar:

```bash
python dtp2p.py simulate \
  --contacts docs/cenarios/cadeia/contacts.txt \
  --messages docs/cenarios/cadeia/messages.txt
```

Parâmetros mínimos:

- `--contacts`;
- `--messages`;
- `--report`;
- `--ttl-default`;
- `--router`.

## Etapa 9: Testes

Criar testes para:

- parser de contatos;
- parser de mensagens;
- roteamento epidêmico;
- TTL;
- métricas;
- execução dos três cenários.

## Etapa 10: Relatório Final da Disciplina

O relatório acadêmico pode conter:

1. introdução;
2. descrição do problema DTN;
3. arquitetura da solução;
4. algoritmo de roteamento epidêmico;
5. cenários testados;
6. resultados e métricas;
7. análise dos resultados;
8. conclusão;
9. possível extensão com PROPHET.

## Checklist de Entrega

- [ ] Código-fonte executável.
- [ ] Simulação baseada em eventos discretos.
- [ ] Módulo de contatos.
- [ ] Módulo de troca P2P.
- [ ] Roteamento epidêmico.
- [ ] TTL por mensagem.
- [ ] Controle de mensagens vistas.
- [ ] Métricas obrigatórias.
- [ ] Três cenários de teste.
- [ ] Documentação de execução.
- [ ] Relatório ou saída final da simulação.
