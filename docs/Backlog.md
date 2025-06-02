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

## 🕰️ Histórico de Versão
| Data       | Versão | Descrição            | Autores                                                                                                                            |
|------------|--------|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 24/04/2025 | 0.1    | Mapeamento inicial do backlog e estrutura | [Ana Luíza Fernandes Alves da Rocha](https://github.com/analufernanndess) e [Tales Rodrigues Gonçalves](https://github.com/TalesRG)|
