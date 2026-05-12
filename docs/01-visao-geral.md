# Visão Geral

## Título

Implementação de uma Rede P2P para Simulação de DTN em Cenários de Alta Latência e Desconexão.

## Problema

Em uma rede DTN, não existe garantia de caminho fim-a-fim entre origem e destino no momento em que uma mensagem é criada. Os nós precisam armazenar mensagens localmente e encaminhá-las quando encontram outros nós no futuro.

No contexto desta atividade, cada nó atua como um par P2P e também como um message ferry: ele guarda mensagens, carrega essas mensagens durante períodos sem contato e as repassa quando encontra outros nós.

## Objetivos Técnicos

- Simular uma rede descentralizada, sem servidor central.
- Modelar contatos intermitentes entre pares de nós.
- Implementar store-and-forward em cada nó.
- Implementar roteamento epidêmico.
- Controlar duplicatas e loops com IDs de mensagens vistas.
- Aplicar TTL por saltos para limitar propagação.
- Calcular métricas de entrega, latência e overhead.

## Escopo Recomendado

A versão principal deve ser uma simulação baseada em eventos discretos. Isso significa que o tempo da rede é simulado por uma fila de eventos ordenada por timestamp, em vez de depender de tempo real, sleep, threads ou relógio do sistema operacional.

Essa escolha deixa os resultados reprodutíveis e facilita os testes dos três cenários exigidos.

## Fora do Escopo da Versão Mínima

- GPS ou mobilidade real.
- Interface gráfica.
- Descoberta automática de peers.
- Criptografia.
- Consenso global.
- Servidor central.
- Garantia forte de entrega.
- Sincronização real entre processos.

## Entidades Principais

| Entidade | Responsabilidade |
|---|---|
| Nó | Armazena mensagens, conhece mensagens vistas e participa de contatos P2P. |
| Mensagem | Representa uma carga enviada de uma origem para um destino. |
| Contato | Define uma janela de conectividade entre dois nós. |
| Simulador | Executa eventos em ordem temporal. |
| Roteador Epidêmico | Decide quais mensagens transferir em um encontro. |
| Coletor de Métricas | Conta entregas, transmissões, latências e overhead. |

## Suposições

- IDs de nós são inteiros positivos.
- O tempo da simulação é representado como número decimal em segundos simulados.
- Uma mensagem pode existir em vários buffers ao mesmo tempo.
- Uma entrega única ocorre quando o destino recebe a mensagem pela primeira vez.
- Cópias posteriores da mesma mensagem no destino não contam como novas entregas.
- TTL é decrementado a cada transmissão entre dois nós.
- Mensagens com TTL igual a zero não são encaminhadas novamente.

