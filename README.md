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
   git clone https://github.com/thomasq/github-monitor.git
   cd github-monitor
   ```

2. **Create environment file**
   ```bash
   cp .env.template .env
   ```

3. **Configure your environment variables**
   Open the `.env` file and set:
   ```
   # Required: GitHub API Token
   GITHUB_TOKEN=your_github_token_here
   
   # Optional: Repositories to monitor
   REPOS="docker/buildx, docker/model-cli"
   
   # Optional: Grafana server configuration
   GF_SERVER_ROOT_URL=https://your-domain.com
   GF_SERVER_DOMAIN=your-domain.com
   GF_SERVER_ENFORCE_DOMAIN=true
   ```

4. **Set permissions** (required for SELinux environments)
   ```bash
   ./set-perms.sh
   ```
5. **generate grafana.ini**
   ```bash
   ./generate-config.sh
   ```
   
6. **Start Grafana**
   ```bash
   docker-compose up -d
   ```

7. **Access the dashboard**
   
   Open http://localhost:3000 in your browser (or your custom domain if configured in .env)

## Configuration

### Environment Variables

The dashboard configuration is controlled through environment variables in your `.env` file:

| Variable | Purpose | Default |
|----------|---------|---------|
| `GITHUB_TOKEN` | GitHub personal access token (required) | None |
| `REPOS` | Comma-separated list of repositories to monitor | None |
| `GF_SERVER_ROOT_URL` | Full URL where Grafana is accessible | http://localhost:3000 |
| `GF_SERVER_DOMAIN` | Domain for Grafana cookies | localhost |
| `GF_SERVER_ENFORCE_DOMAIN` | Enforce domain for security | true |

You can add other Grafana configuration options with the `GF_` prefix. See the [Grafana documentation](https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/) for all available options.

### Limiting Repository Access

The dashboard shows repositories based on your `.env` configuration:

1. **Set repositories in your .env file**
   ```
   REPOS="YaLTeR/niri, YaLTeR/wl-clipboard-rs, hyperlight-dev/hyperlight, docker/buildx, docker/model-cli"
   ```

2. **Run the update script**
   ```bash
   ./update-dashboard.sh
   ```

### Custom Domain Configuration

To serve the dashboard on a custom domain, set these variables in your `.env` file:

```
GF_SERVER_ROOT_URL=https://your-domain.com
GF_SERVER_DOMAIN=your-domain.com
GF_SERVER_ENFORCE_DOMAIN=true
```

The Docker Compose file and Grafana configuration will automatically use these settings.

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
- Configurable domain enforcement via environment variables

## Customization

### Adding Custom Dashboards

Place your custom dashboard JSON files in the `dashboards` directory and they will be automatically loaded.

### Modifying Datasource Configuration

Edit `provisioning/datasources/datasource.yaml` to modify the GitHub datasource settings. The GitHub token is automatically injected from your `.env` file.

See the [Grafana configuration documentation](https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/) for all available options.

## Testing

### Running Tests Locally

1. Run configuration validation:
```bash
./test/validate-config.sh
```

2. Run integration tests:
```bash
./test/integration-test.sh
```

### Continuous Integration

The project uses GitHub Actions for CI/CD. Every push and pull request triggers:
- Docker configuration validation
- Container build testing
- Integration tests
- Health checks

View the status of CI runs in the GitHub Actions tab.

## Troubleshooting

### Configuration Issues

If your configuration isn't being applied properly:

1. Check that your `.env` file exists and has the correct permissions
2. Verify that Docker Compose is loading the `.env` file
3. Restart the container to apply changes: `docker-compose restart`

### Access Issues

If you can't access your dashboard:

1. Check that the `GF_SERVER_ROOT_URL` matches how you're accessing Grafana
2. Ensure port 3000 is accessible (or whichever port you've configured)
3. Check Docker logs: `docker-compose logs grafana`

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
