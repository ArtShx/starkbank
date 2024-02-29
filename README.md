# StarkBank skill test
Integração com servidor StarkBank

1: Emissão de boletos (entre 8 a 12) a cada 3 horas para pessoas aleatórias por 24h
    Imaginar que são boletos reais, para clientes da minha própria empresa e a starkbank é o meu banco


2: Receber um callback webhook dos créditos recebidos (da tarefa 1) e transferir o montante recebido (subtraindo eventuais taxas) para a conta da Stark Bank


## TODO
- [x] Create a package for starkbank api integration;
- [ ] Create tests for `services/` and finish development of both services -> waiting for `sandbox` access;
- [ ] Add shell script to setup a cron job;
- [x] Add CI automated tests on commit, run tests and coverage report;
- [x] Setup a GCP freetier account (maybe use Terraform or other IaC tool?);
- [ ] Add CD automated deploy on GCP;
- [ ] Deploy `services` and the `starkbank_integration` package into a cloud provider;

