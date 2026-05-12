# Interface de Execução

## Interface Recomendada

Embora o enunciado mostre comandos por nó, a implementação recomendada para a versão mínima é uma CLI de simulação:

```bash
python dtp2p.py simulate \
  --contacts docs/cenarios/cadeia/contacts.txt \
  --messages docs/cenarios/cadeia/messages.txt \
  --router epidemic \
  --report reports/cadeia-report.json
```

## Comando `simulate`

Responsável por executar uma simulação completa.

Parâmetros:

| Parâmetro | Obrigatório | Descrição |
|---|---|---|
| `--contacts` | sim | Caminho para o arquivo de contatos. |
| `--messages` | sim | Caminho para mensagens iniciais. |
| `--nodes` | não | Lista opcional de IDs de nós. |
| `--ttl-default` | não | TTL usado quando a mensagem não informar TTL. |
| `--router` | não | Algoritmo de roteamento: `epidemic` ou `prophet`. |
| `--report` | não | Caminho do relatório JSON. |
| `--log-level` | não | Nível de log: `debug`, `info`, `warning`. |

Exemplo:

```bash
python dtp2p.py simulate \
  --contacts docs/cenarios/denso/contacts.txt \
  --messages docs/cenarios/denso/messages.txt \
  --router epidemic \
  --ttl-default 5 \
  --report reports/denso-report.json
```

Para executar com PROPHET:

```bash
python dtp2p.py simulate \
  --contacts docs/cenarios/denso/contacts.txt \
  --messages docs/cenarios/denso/messages.txt \
  --router prophet \
  --report reports/denso-prophet-report.json
```

## Comando `send`

Opcional para manter compatibilidade com a interface do enunciado.

```bash
python dtp2p.py send --from 1 --to 4 --msg "ola" --ttl 5
```

Na arquitetura baseada em eventos, esse comando pode apenas adicionar uma linha a um arquivo de mensagens ou imprimir uma mensagem formatada para uso em `messages.txt`.

Exemplo de saída:

```text
0.0, 1, 4, 5, ola
```

## Modo por Nó

Se a implementação usar processos reais, a interface pode seguir o enunciado:

```bash
python dtp2p.py node --id 1 --port 5001 --contacts contacts.txt
python dtp2p.py node --id 2 --port 5002 --contacts contacts.txt
python dtp2p.py node --id 3 --port 5003 --contacts contacts.txt
```

Envio:

```bash
python dtp2p.py send --from 1 --to 4 --msg "ola"
```

Essa variação exige descoberta das portas dos nós. Para evitar servidor central, as portas podem ser definidas em arquivo:

```text
1, 127.0.0.1, 5001
2, 127.0.0.1, 5002
3, 127.0.0.1, 5003
4, 127.0.0.1, 5004
```

## Logs

O log deve mostrar os eventos principais:

```text
[sim] t=0.0 criada m-1-0001 origem=1 destino=4 ttl=5
[1] t=1.0 contato com 2
[1] t=1.0 enviando m-1-0001 para 2 ttl=5->4
[2] t=1.0 recebeu m-1-0001 destino=4 ttl=4
[2] t=4.0 contato com 3
[2] t=4.0 enviando m-1-0001 para 3 ttl=4->3
```

## Códigos de Saída

| Código | Significado |
|---|---|
| `0` | Simulação finalizada com sucesso. |
| `1` | Erro de argumentos na CLI. |
| `2` | Erro ao ler arquivos de entrada. |
| `3` | Erro de validação dos dados. |
| `4` | Erro inesperado durante a simulação. |

## Comandos de Teste Esperados

```bash
python dtp2p.py simulate --contacts docs/cenarios/denso/contacts.txt --messages docs/cenarios/denso/messages.txt
python dtp2p.py simulate --contacts docs/cenarios/esparso/contacts.txt --messages docs/cenarios/esparso/messages.txt
python dtp2p.py simulate --contacts docs/cenarios/cadeia/contacts.txt --messages docs/cenarios/cadeia/messages.txt
python dtp2p.py simulate --contacts docs/cenarios/denso/contacts.txt --messages docs/cenarios/denso/messages.txt --router prophet
```
