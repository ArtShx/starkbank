Integração com servidor StarkBank

1: Emissão de boletos (entre 8 a 12) a cada 3 horas para pessoas aleatórias por 24h
    Imaginar que são boletos reais, para clientes da minha própria empresa e a starkbank é o meu banco


2: Receber um callback webhook dos créditos recebidos (da tarefa 1) e transferir o montante recebido (subtraindo eventuais taxas) para a conta da Stark Bank


- Adicionar teste unitários
- Analisar performance
- Legibilidade

- Deploy da solução em cloud


---

Criar package com código base para integração com starkbank
    Mudar `src/` para `starkbank_impl` (ou algo similar)
    Adicionar código referentes ao package (setup.py)

Criar IaC que utiliza package e lambdas para executar cada task
