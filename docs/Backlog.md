# 🗂️ Backlog do Projeto

## 🎯 Objetivo
Este backlog tem como objetivo organizar e documentar os requisitos, épicos e histórias de usuário para o desenvolvimento do dashboard de monitoramento de projetos no GitHub.

---

## ✅ Requisitos Funcionais
- **RF01**: O sistema deve disponibilizar painéis pré-configurados para monitorar atividades do GitHub.
- **RF02**: O sistema deve permitir visualizar estatísticas de múltiplos repositórios dentro de uma organização.
- **RF03**: O sistema deve permitir filtrar o acesso aos repositórios exibidos no dashboard.
- **RF04**: O sistema deve exibir métricas granulares como issues, pull requests, releases e commits.
- **RF05**: O sistema deve permitir acesso anônimo com permissões restritas.
- **RF06**: O sistema deve possibilitar a exportação de relatórios em formatos PDF e Excel.
- **RF07**: O sistema deve ser compatível com implantação via Docker Compose/Kubernetes.
- **RF08**: O sistema deve permitir a configuração de um domínio personalizado para acesso ao dashboard.

---

## 🛡️ Requisitos Não Funcionais
- **RNF01**: O sistema deve ser implantável com alta facilidade usando Docker Compose/Kubernetes.
- **RNF02**: O sistema deve ser responsivo, adaptando-se a diferentes tamanhos de tela.
- **RNF03**: O sistema deve seguir boas práticas de código aberto, incluindo documentação técnica e política de contribuições.
- **RNF04**: O sistema deve ter compatibilidade cross-browser (Chrome, Firefox, Edge).
- **RNF05**: O sistema deve possuir integração contínua com execução de testes automatizados no GitHub Actions.

---

## 🏗️ Épicos
- **EP01**: Montar infraestrutura de monitoramento de repositórios GitHub.
- **EP02**: Implementar funcionalidade de filtragem e visualização personalizada de dados.
- **EP03**: Criar recurso de exportação de relatórios.
- **EP04**: Configurar acesso anônimo e permissões de usuário.
- **EP05**: Automatizar implantação via Docker Compose/Kubernetes.
- **EP06**: Configurar domínio personalizado para acesso externo ao dashboard.

---

## 👤 Histórias de Usuário
| ID | História de Usuário |
|:--|:--|
| **US01** | Como usuário, quero visualizar painéis prontos para acompanhar rapidamente a atividade dos repositórios. |
| **US02** | Como administrador, quero filtrar quais repositórios aparecem para garantir que apenas projetos relevantes sejam exibidos. |
| **US03** | Como colaborador, quero acompanhar métricas específicas (issues, pull requests, commits) para entender a evolução dos projetos. |
| **US04** | Como visitante anônimo, quero visualizar o dashboard público com permissões limitadas para acessar apenas informações liberadas. |
| **US05** | Como administrador, quero exportar dados do dashboard para PDF ou Excel para gerar relatórios de acompanhamento. |
| **US06** | Como desenvolvedor, quero subir o ambiente rapidamente usando Docker Compose/Kubernetes para agilizar a instalação. |
| **US07** | Como administrador, quero configurar um domínio personalizado para que o dashboard seja acessível em um endereço próprio. |

---

## 📝 Tarefas

| ID  | US Relacionada | Descrição |
|-----|----------------|-----------|
| T01 | US01 | Criar dashboard "Visão Geral" com os campos mais relevantes(commits, PRs, issues) |
| T02 | US01 | Desenvolver template de painéis reutilizáveis por repositório |
| T03 | US02 | Criar filtro multi-seleção na interface |
| T04 | US03 | Construir painel com base nos status das issues (abertas/fechadas/tags) |
| T05 | US03 | Desenvolver visualização de PRs por status |
| T06 | US03 | Implementar gráfico de commits por autor/branch |
| T07 | US03 | Adicionar seletor de intervalo temporal |
| T08 | US04 | Desenvolver controle de acesso baseado em permissões |
| T09 | US04 | Desenvolver versão simplificada de dashboards públicos |
| T10 | US05 | Permitir exportação PDF/Excel/CSV |
| T11 | US05 | Implementar botão "Exportar" nos painéis |
| T12 | US05 | Criar templates de relatórios formatados |
| T13 | US05 | Configurar exportações automáticas |
| T14 | US06 | Desenvolver Dockerfile para stack Grafana + plugins |
| T15 | US06 | Criar docker-compose.yml com volumes persistentes |
| T16 | US06 | Configurar variáveis de ambiente para credenciais |
| T17 | US06 | Documentar processo de inicialização containerizada |
| T18 | US07 | Configurar proxy reverso (Nginx/Caddy) |
| T19 | US07 | Implementar certificado SSL |
| T20 | US07 | Definir variável `domain` no grafana.ini |
| T21 | US07 | Configurar registros DNS para subdomínio dedicado |

---

## 🕰️ Histórico de Versão
| Data       | Versão | Descrição            | Autores                                                                                                                            |
|------------|--------|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 24/04/2025 | 0.1    | Mapeamento inicial do backlog e estrutura | [Ana Luíza Fernandes Alves da Rocha](https://github.com/analufernanndess) e [Tales Rodrigues Gonçalves](https://github.com/TalesRG)|
| 31/05/2025 | 0.2    | Derivação das USs em tarefas | [Vitor Borges](https://github.com/VitorB2002)|
