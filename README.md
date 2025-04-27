# GitHub Dashboard for Grafana

A ready-to-use GitHub monitoring dashboard for Grafana that provides comprehensive insights into GitHub repositories, issues, pull requests, and more. This project makes it easy to set up and customize dashboards for specific GitHub organizations and repositories.

## Features

- **Pre-configured Dashboards**: Ready-to-use dashboards for tracking GitHub activity
- **Organization Overview**: View statistics across multiple repositories in an organization
- **Repository Filtering**: Limit dashboard access to specific repositories
- **Granular Metrics**: Track issues, pull requests, releases, commits, and more
- **Anonymous Access**: Configure for public viewing with restricted permissions
- **Docker Ready**: Easily deploy with Docker Compose

## Requirements

- Docker and Docker Compose
- GitHub Personal Access Token
- Bash (for running setup scripts)
- jq (for repository filtering script)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/github-dashboard.git
   cd github-dashboard
   ```

2. **Create environment file**
   ```bash
   cp .env.template .env
   ```

3. **Add your GitHub token to the .env file**
   ```bash
   echo "GITHUB_TOKEN=your_github_token_here" > .env
   ```

4. **Set permissions** (required for SELinux environments)
   ```bash
   ./set-perms.sh
   ```

5. **Start Grafana**
   ```bash
   docker-compose up -d
   ```

6. **Access the dashboard**
   
   Open http://localhost:3000 in your browser

## Configuration

### Limiting Repository Access

By default, the dashboard shows all repositories from the configured organizations. To limit access to specific repositories:

1. **Set repositories in an environment variable**
   ```bash
   export REPOS="YaLTeR/niri, YaLTeR/wl-clipboard-rs, hyperlight-dev/hyperlight, docker/buildx, docker/model-cli"
   ```

2. **Run the update script**
   ```bash
   ./update-dashboard.sh
   ```

### Custom Domain Configuration

To serve the dashboard on a custom domain:

1. Edit `docker-compose.yml` and update:
   ```yaml
   GF_SERVER_ROOT_URL=https://your-domain.com
   ```

2. Edit `grafana.ini` and update:
   ```ini
   [server]
   root_url = https://your-domain.com
   domain = your-domain.com
   ```

## Dashboard Overview

This project includes two main dashboards:

### GitHub Dashboard

Provides detailed metrics for a specific repository:
- Release and tag counts
- Pull request metrics (count, open time)
- Issue metrics (open/closed counts, resolution time)
- Historical data tables for commits, issues, PRs
- Contributor information

### GitHub Organization Dashboard

Provides an overview of multiple repositories in an organization:
- Releases per repository
- Issues created per repository
- Pull requests per repository
- Active issues and PRs

## Security Features

This configuration is designed with security in mind:
- Anonymous access with viewer-only permissions
- No login form or API access for anonymous users
- CSRF protection with strict cookie settings
- Rate limiting for dashboard refreshes

## Customization

### Adding Custom Dashboards

Place your custom dashboard JSON files in the `dashboards` directory and they will be automatically loaded.

### Modifying Datasource Configuration

Edit `provisioning/datasources/datasource.yaml` to modify the GitHub datasource settings.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgements

- Built with [Grafana](https://grafana.com/)
- Uses the [GitHub Datasource for Grafana](https://grafana.com/grafana/plugins/grafana-github-datasource/)
