# Roadmap - GitHub Monitor

Este roadmap apresenta a visão de evolução do projeto, agrupando objetivos em épicos e suas respectivas features, com informações de status, prioridade e critérios de conclusão, além de listar quais dependências foram escolhidas para o projeto e suas respectivas versões.

---

## 🗂️ Legenda de Status para os épicos e features
- ✅ Concluído
- 🚧 Em andamento
- 📝 Planejado

## 📊 Lista das dependências utilizadas
- Grafana 11.6.0
- Github datasource 2.1.4

---

## 🧩 Épicos e Features

### Épico 1: Coleta e Organização de Dados do GitHub (📝)

| Feature | Status | Prioridade | Complexidade |
|:--------|:-------|:-----------|:-------------|
| Coletar Issues, PRs e Commits via API | 📝 | Alta | Fácil |
| Suporte a múltiplos repositórios | 📝 | Alta | Médio |
| Coletar métricas de Stars, Forks e Watchers | 📝 | Média | Médio |
| Implementar coleta incremental (otimização API) | 📝 | Alta | Difícil |

**Definition of Done:**
- Dados de Issues, PRs, Commits, Stars, Forks e Watchers armazenados de forma consistente.
- Múltiplos repositórios configuráveis via `.env`.
- Redução de requisições para evitar rate limits da GitHub API.

---

### Épico 2: Dashboards no Grafana (🚧)

| Feature | Status | Prioridade | Complexidade |
|:--------|:-------|:-----------|:-------------|
| Dashboard inicial de métricas principais | 📝 | Alta | Médio |
| Dashboards por organização e por repositório | 📝 | Média | Médio |
| Dashboards históricos (tendência de atividade) | 📝 | Alta | Difícil |
| Suporte a múltiplos temas (Dark/Light Mode) | 📝 | Baixa | Fácil |

**Definition of Done:**
- Dashboards acessíveis após deploy padrão.
- Visualizações históricas funcionais para no mínimo 12 meses de dados.
- Suporte a visualização Light/Dark via configuração.

---

### Épico 3: Configuração e Implantação (📝)

| Feature | Status | Prioridade | Complexidade |
|:--------|:-------|:-----------|:-------------|
| Deploy via Docker Compose | 📝 | Alta | Fácil |
| Templates de deploy para Kubernetes | 📝 | Média | Difícil |
| Gerenciamento de configurações via `.env` | 📝 | Alta | Fácil |
| Script de instalação automático | 📝 | Média | Médio |

**Definition of Done:**
- Docker Compose rodando sem necessidade de configuração manual extra.
- Helm Chart ou YAMLs prontos para deploy no Kubernetes.
- Script capaz de rodar `setup.sh` para subir ambiente completo.

---

### Épico 4: Monitoramento e Alertas (📝)

| Feature | Status | Prioridade | Complexidade |
|:--------|:-------|:-----------|:-------------|
| Alertas no Grafana para eventos críticos | 📝 | Média | Médio |
| Integração com Slack/Email para alertas | 📝 | Baixa | Médio |
| Painel "Health Overview" por repositório | 📝 | Média | Médio |

**Definition of Done:**
- Definição de alertas no Grafana configuráveis via dashboard.
- Envio de alertas externos opcional (Slack, Email).

---

## 📋 Requisitos para o MVP (Minimum Viable Product)

Essenciais para primeira versão pública:

- [ ] Coletar Issues, PRs e Commits
- [ ] Deploy via Docker Compose
- [ ] Dashboard inicial com principais métricas
- [ ] Configuração via `.env`

---

## 🌟 Melhorias Futuras

- Suporte a múltiplos repositórios
- Dashboards históricos e temáticos
- Deploy em Kubernetes
- Alertas automáticos no Grafana
- Integração com Slack/Email
- Cache local para otimização de chamadas API
- Suporte a múltiplas plataformas (GitLab, Bitbucket)

---

## 📅 Timeline sugerida

| Mês         | Entregas Prioritárias                             |
|-------------|---------------------------------------------------|
| Maio 2025   | Dashboards históricos + Suporte a múltiplos repositórios |
| Junho 2025  | Deploy Kubernetes + Alertas no Grafana             |
| Julho 2025  | Integrações externas + Melhorias de performance    |

---

## ✍️ Notas

- As prioridades e entregas podem mudar conforme feedback da comunidade e crescimento do projeto.
- Sugestões são sempre bem-vindas! Veja [contribuir.md](./docs/contribuir.md) para colaborar.

## 🕰️ Histórico de Versão
| Data       | Versão | Descrição            | Autores                                                                                                                            |
|------------|--------|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 27/04/2025 | 0.1    | Criação do Roadmap | [Yan Luca Viana de Araújo Fontenele](https://github.com/yan-luca) e [Gabriel Marques de Souza](https://github.com/GabrielMS00)|