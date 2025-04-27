# 🧩 Funcionamento do Projeto

## 🎯 Objetivo:
Um painel de monitoramento do GitHub pronto para uso no Grafana que oferece insights abrangentes sobre repositórios do GitHub, issues, pull requests e muito mais. Este projeto facilita a configuração e personalização de painéis para organizações e repositórios específicos do GitHub.

## 	🛠️ Funcionalidades:
### 🖥️ Painéis pré-configurados:
Painéis prontos para uso para monitorar a atividade no GitHub

### 🧭 Visão geral da organização: 
Visualize estatísticas de vários repositórios dentro de uma organização

### 🗂️ Filtragem de repositórios:
Limite o acesso do painel a repositórios específicos

### 📊 Métricas granulares:
Acompanhe issues, pull requests, releases, commits e mais

### 🕵️‍♂️ Acesso anônimo:
Configure para visualização pública com permissões restritas

### 🐳 Compatível com Docker:
Faça a implantação facilmente com Docker Compose

## 📋 Requisitos
- Docker and Docker Compose
- Token de Acesso Pessoal do GitHub
- Bash (para executar scripts de configuração)
- jq (para o script de filtragem de repositórios)

## 🚀 Início Rápido

1. Fork do Repositório:
- Faça um Fork deste repositório no GitHub.
- Clone o seu Fork localmente:

```bash
git clone https://github.com/thmasq/github-monitor.git
cd github-dashboard
```

2. Crie o arquivo de ambiente

```bash
cp .env.template .env
```

3. Adicione seu token do GitHub ao arquivo .env

```bash
# Required: GitHub API Token
GITHUB_TOKEN=your_github_token_here

# Optional: Repositories to monitor
REPOS="docker/buildx, docker/model-cli"

# Optional: Grafana server configuration
GF_SERVER_ROOT_URL=https://your-domain.com
GF_SERVER_DOMAIN=your-domain.com
GF_SERVER_ENFORCE_DOMAIN=true
```

4. Configure as permissões (necessário para ambientes com SELinux)

```bash
./set-perms.sh
```

5. Gere o grafana.ini

```bash
./generate-config.sh
```


6. Inicie o Grafana

```bash
docker-compose up -d
```

7. Acesse o dashboard
Abra http://localhost:3000 no seu navegador.

## ⚙️ Configuração

### 🔒 Limitando o Acesso aos Repositórios

Por padrão, o dashboard exibe todos os repositórios das organizações configuradas. Para limitar o acesso a repositórios específicos:

1. **Defina os repositórios em uma variável de ambiente**

````bash
export REPOS="YaLTeR/niri, YaLTeR/wl-clipboard-rs, hyperlight-dev/hyperlight, docker/buildx, docker/model-cli"
````

2. Execute o script de atualização

````bash
./update-dashboard.sh
````

### 🌐 Configuração de Domínio Personalizado
Para disponibilizar o dashboard em um domínio personalizado:

1. Edite o arquivo *docker-compose.yml* e atualize:

````yaml
GF_SERVER_ROOT_URL=https://seu-dominio.com
````

2. Edite o arquivo *grafana.ini* e atualize:

````ini
[server]
  root_url = https://seu-dominio.com
  domain = seu-dominio.com

````

## 📊 Visão Geral do Dashboard

Este projeto inclui dois dashboards principais:

### GitHub Dashboard

Fornece métricas detalhadas para um repositório específico:

- Contagem de releases e tags
- Métricas de pull requests (quantidade, tempo de abertura)
- Métricas de issues (quantidade abertas/fechadas, tempo de resolução)
- Tabelas de dados históricos para commits, issues e pull requests
- Informações sobre colaboradores

### GitHub Organization Dashboard

Fornece uma visão geral de múltiplos repositórios em uma organização:

- Releases por repositório
- Issues criadas por repositório
- Pull requests por repositório
- Issues e pull requests ativas

## 🔒 Recursos de Segurança

Esta configuração foi projetada com a segurança em mente:

- Acesso anônimo com permissões apenas de visualização
- Sem formulário de login ou acesso à API para usuários anônimos
- Proteção CSRF com configurações rígidas de cookies
- Limitação de taxa para atualizações do dashboard

---

## 🎨 Personalização

### Adicionando Dashboards Personalizados

Coloque seus arquivos JSON de dashboards personalizados no diretório `dashboards` e eles serão carregados automaticamente.

### Modificando a Configuração da Fonte de Dados

Edite o arquivo `provisioning/datasources/datasource.yaml` para modificar as configurações da fonte de dados do GitHub.

---

## 📜 Licença

Este projeto é licenciado sob a Licença Pública Geral GNU versão 3.0 — veja o arquivo [licença](LICENSE) para mais detalhes.

## 🕰️ Histórico de Versão
| Data       | Versão | Descrição                            | Autores                                                                                                                            |
|------------|--------|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| 24/04/2025 | 0.1    | Adicionando Funcionamento do projeto | [Ana Luíza Fernandes Alves da Rocha](https://github.com/analufernanndess) e [Tales Rodrigues Gonçalves](https://github.com/TalesRG)|

