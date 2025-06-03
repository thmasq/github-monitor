# GitHub Dashboard for Grafana

A ready-to-use GitHub monitoring dashboard for Grafana that provides comprehensive insights into GitHub repositories, issues, pull requests, and more. This project makes it easy to set up and customize dashboards for specific GitHub organizations and repositories.
Example instance running [here](https://grafana.tantalius.com).

## Quick Start

```bash
# Clone and setup
git clone https://github.com/thomasq/github-monitor.git
cd github-monitor

# Automated setup (one command)
make quick-start
```

Access your dashboard at http://localhost:3000

## Features

- **Pre-configured Dashboards** - Ready-to-use GitHub monitoring
- **Multi-Repository Support** - Track multiple repos and organizations
- **Smart Filtering** - Configurable repository access control
- **Full Automation** - Python scripts handle all configuration
- **Docker Ready** - One-command deployment
- **Secure Anonymous Access** - Public viewing with restricted permissions

## Requirements

- Docker and Docker Compose
- Python 3.7+
- GitHub Personal Access Token
- Make (optional, for automation)

## Installation Methods

### Method 1: Automated (Recommended)

```bash
make install setup generate start
```

### Method 2: Interactive Setup

```bash
pip install -r requirements.txt
python3 interactive_setup.py
docker-compose up -d
```

### Method 3: Manual Configuration

```bash
cp .env.template .env
# Edit .env with your GitHub token and repositories
python3 generate_provisioning.py
python3 update_dashboards.py
docker-compose up -d
```

## Configuration

Set these in your `.env` file:

```bash
# Required
GITHUB_TOKEN=your_github_token_here
REPOS="docker/buildx, kubernetes/kubernetes, grafana/grafana"

# Optional
GF_SERVER_ROOT_URL=https://your-domain.com
GF_SERVER_DOMAIN=your-domain.com
```

## Python Automation Scripts

| Script                     | Purpose                                   |
| :------------------------- | :---------------------------------------- |
| `interactive_setup.py`     | Interactive configuration wizard          |
| `generate_provisioning.py` | Generate Grafana provisioning files       |
| `update_dashboards.py`     | Update dashboards with repository filters |
| `validate_backlog.py`      | Validate complete system setup            |

## Available Dashboards

### GitHub Dashboard

- Repository metrics (issues, PRs, commits)
- Contributor information
- Release and tag tracking
- Historical data tables

### GitHub Organization Dashboard

- Multi-repository overview
- Organization-wide statistics
- Active issues and PRs across repos

## Management Commands

```bash
# System management
make start          # Start the dashboard
make stop           # Stop the dashboard  
make restart        # Restart services
make logs           # View Grafana logs
make status         # Check container status

# Configuration
make setup          # Interactive setup
make generate       # Generate provisioning
make update         # Update dashboards
make validate       # Validate configuration

# Maintenance
make test           # Run integration tests
make backup         # Backup configuration
make clean          # Clean temporary files
```

## Monitoring Capabilities

- **Issues**: Created, open, closed, resolution time
- **Pull Requests**: Created, active, merge time
- **Releases**: Version tracking and deployment frequency
- **Contributors**: Team activity and contributions
- **Organizations**: Multi-repo statistics and trends

## Filtering Options

- Filter by specific repositories
- Organization-level views
- Time-based analysis
- Label and milestone filtering

## Testing

```bash
# Validate setup
make test

# Check specific components
python3 validate_backlog.py
./test/integration-test.sh
```

## Project Structure

```
├── Python Scripts
│   ├── interactive_setup.py      # Configuration wizard
│   ├── generate_provisioning.py  # Provisioning generator
│   ├── update_dashboards.py      # Dashboard updater
│   └── validate_backlog.py       # System validator
├── Dashboards
│   ├── github.json               # Main dashboard
│   └── github-organization.json  # Organization dashboard
├── Provisioning (auto-generated)
│   ├── datasources/              # GitHub datasource config
│   ├── dashboards/               # Dashboard provisioning
│   └── access-control/           # Security settings
└── Configuration
    ├── docker-compose.yml        # Container setup
    ├── .env.template            # Configuration template
    └── Makefile                 # Automation commands
```

## Troubleshooting

### Common Issues

**Dashboard not loading?**

```bash
make logs
make validate
```

**Repository filtering not working?**

```bash
make update restart
```

**Grafana won't start?**

```bash
make clean start
```

**Need to reconfigure?**

```bash
make setup generate restart
```

If you can't access your dashboard:

1. Check that the `GF_SERVER_ROOT_URL` matches how you're accessing Grafana
2. Ensure port 3000 is accessible (or whichever port you've configured)
3. Check Docker logs: `docker-compose logs grafana`

## Security

- Anonymous access with viewer-only permissions
- No API access for anonymous users
- Repository access controlled via configuration
- CSRF protection enabled
- Secure cookie settings

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
