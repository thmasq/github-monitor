# Fluxograma de Dados

```mermaid
graph TD
    %% Configuração Inicial
    A[Usuário] -->|Clone do Repositório| B[github-monitor]
    B --> C[Configuração .env]
    C -->|GITHUB_TOKEN<br/>REPOS<br/>GF_SERVER_*| D[Variáveis de Ambiente]
    
    %% Scripts de Setup
    D --> E[Scripts de Configuração]
    E --> E1[./set-perms.sh<br/>Permissões SELinux]
    E --> E2[./generate-config.sh<br/>Gera grafana.ini]
    E --> E3[./update-dashboard.sh<br/>Atualiza Dashboards]
    
    %% Inicialização do Sistema
    E1 --> F[Docker Compose]
    E2 --> F
    F -->|docker-compose up -d| G[Container Grafana]
    
    %% Fontes de Dados
    H[GitHub API] -->|Personal Access Token| I[GitHub Datasource]
    D -->|GITHUB_TOKEN| I
    
    %% Processamento de Dados
    I -->|Pull de Dados| J[Métricas GitHub]
    J --> J1[Issues<br/>- Abertas/Fechadas<br/>- Tempo de Resolução<br/>- Contadores]
    J --> J2[Pull Requests<br/>- Contadores<br/>- Tempo de Abertura<br/>- Status]
    J --> J3[Releases<br/>- Contadores por Repo<br/>- Tags]
    J --> J4[Commits<br/>- Histórico<br/>- Contribuidores]
    J --> J5[Repositórios<br/>- Filtrados por REPOS<br/>- Estatísticas]
    
    %% Sistema de Dashboards
    K[Provisioning System]
    K --> K1[provisioning/datasources/<br/>datasource.yaml]
    K --> K2[dashboards/<br/>Dashboard JSONs]
    
    %% Configuração de Dashboards
    J1 --> L[Repository Dashboard]
    J2 --> L
    J3 --> L
    J4 --> L
    L -->|Métricas Detalhadas<br/>de Repositório Específico| M[Grafana UI]
    
    J1 --> N[Organization Dashboard]
    J3 --> N
    J5 --> N
    N -->|Visão Geral<br/>Múltiplos Repositórios| M
    
    %% Sistema de Segurança
    O[Configurações de Segurança]
    O --> O1[Acesso Anônimo<br/>Somente Visualização]
    O --> O2[Proteção CSRF<br/>Cookies Seguros]
    O --> O3[Rate Limiting<br/>Refresh de Dashboards]
    O --> O4[Domain Enforcement<br/>GF_SERVER_ENFORCE_DOMAIN]
    
    O1 --> M
    O2 --> M
    O3 --> M
    O4 --> M
    
    %% Acesso Final
    M -->P[Dashboard Interativo]
    P --> P1[Visualizações<br/>- Gráficos<br/>- Tabelas<br/>- Métricas]
    P --> P2[Filtros<br/>- Por Repositório<br/>- Por Período<br/>- Por Tipo]
    
    %% Atualizações e Manutenção
    Q[Sistema de Atualização]
    Q --> Q1[./test/validate-config.sh<br/>Validação]
    Q --> Q2[./test/integration-test.sh<br/>Testes Integração]
    Q --> Q3[GitHub Actions CI/CD<br/>- Build Testing<br/>- Health Checks]
    
    %% Logs e Monitoramento
    R[Logs e Debug]
    G --> R
    R -->|docker-compose logs grafana| S[Troubleshooting]
    
    %% Estilos
    classDef configClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000,font-weight:bold
    classDef dataClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000,font-weight:bold
    classDef systemClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000,font-weight:bold
    classDef uiClass fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000,font-weight:bold
    classDef securityClass fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000,font-weight:bold
    
    class A,C,D,E,E1,E2,E3 configClass
    class H,I,J,J1,J2,J3,J4,J5 dataClass
    class F,G,K,K1,K2,Q,Q1,Q2,Q3,R systemClass
    class L,N,M,P,P1,P2 uiClass
    class O,O1,O2,O3,O4 securityClass
```

## Descrição dos Componentes

### 🔧 Configuração Inicial (Azul)
- **Clone do Repositório**: Primeira etapa onde o usuário clona o projeto
- **Configuração .env**: Definição das variáveis de ambiente essenciais
- **Scripts de Setup**: Automação da configuração do sistema

### 📊 Fontes de Dados (Roxo)
- **GitHub API**: Fonte primária de dados através de Personal Access Token
- **Métricas Coletadas**:
  - Issues (abertas/fechadas, tempo de resolução)
  - Pull Requests (contadores, tempo de abertura, status)
  - Releases (contadores por repositório, tags)
  - Commits (histórico, contribuidores)
  - Repositórios (estatísticas filtradas)

### ⚙️ Sistema (Verde)
- **Docker Compose**: Orquestração de containers
- **Grafana Container**: Ambiente de execução principal
- **Provisioning System**: Configuração automatizada de datasources e dashboards
- **CI/CD**: Automação de testes e validação

### 🎨 Interface de Usuário (Laranja)
- **Repository Dashboard**: Métricas detalhadas de repositório específico
- **Organization Dashboard**: Visão geral de múltiplos repositórios
- **Grafana UI**: Interface principal com visualizações interativas

### 🔒 Segurança (Vermelho)
- **Acesso Anônimo Controlado**: Visualização sem autenticação com permissões limitadas
- **Proteção CSRF**: Segurança contra ataques cross-site
- **Rate Limiting**: Controle de frequência de atualizações
- **Domain Enforcement**: Restrição de acesso por domínio

## Fluxo de Dados Principal

1. **Inicialização**: Usuário configura variáveis de ambiente e executa scripts de setup
2. **Coleta**: Sistema puxa dados da API do GitHub usando token de acesso
3. **Processamento**: Dados são organizados em métricas específicas
4. **Visualização**: Métricas são apresentadas em dashboards Grafana
5. **Interação**: Usuário acessa dashboards através do navegador

## Variáveis de Ambiente Principais

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `GITHUB_TOKEN` | Token de acesso pessoal do GitHub | ✅ |
| `REPOS` | Lista de repositórios para monitorar | ❌ |
| `GF_SERVER_ROOT_URL` | URL completa do Grafana | ❌ |
| `GF_SERVER_DOMAIN` | Domínio do servidor Grafana | ❌ |

## Scripts Disponíveis

- `./set-perms.sh`: Configura permissões para ambientes SELinux
- `./generate-config.sh`: Gera arquivo de configuração do Grafana
- `./update-dashboard.sh`: Atualiza configurações dos dashboards
- `./test/validate-config.sh`: Valida configurações
- `./test/integration-test.sh`: Executa testes de integração

## 🕰️ Histórico de Versão
| Data       | Versão | Descrição            | Autores                                                                                                                            |
|------------|--------|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 02/06/2025 | 0.1    | Criação do Fluxograma dos Dados | [Yan Luca Viana de Araújo Fontenele](https://github.com/yan-luca) |