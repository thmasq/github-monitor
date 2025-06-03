#!/usr/bin/env python3
"""
Grafana Automatic Provisioning Document Generator
Implements functional requirements RF01, RF02, RF03 from the backlog
"""

import os
import yaml
import json
from pathlib import Path
from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GrafanaConfig:
    """Main Grafana config"""

    github_token: str
    organizations: List[str]
    repositories: List[str]
    server_root_url: str = "http://localhost:3000"
    server_domain: str = "localhost"
    enforce_domain: bool = True


@dataclass
class DatasourceConfig:
    """GitHub data source config"""

    name: str = "GitHub"
    type: str = "grafana-github-datasource"
    access: str = "proxy"
    is_default: bool = True
    editable: bool = False


@dataclass
class DashboardConfig:
    """Dashboard config"""

    provider_name: str = "default"
    org_id: int = 1
    folder: str = ""
    type: str = "file"
    disable_deletion: bool = True
    update_interval_seconds: int = 10
    allow_ui_updates: bool = False
    path: str = "/var/lib/grafana/dashboards"


@dataclass
class AccessControlConfig:
    """Access control config"""

    role_name: str = "restricted_viewer"
    description: str = (
        "A viewer with no access to the Grafana API except for viewing dashboards"
    )
    assignment_name: str = "read_only_anon"
    target: str = "anonymous"


class GrafanaProvisioningGenerator:
    """
    Core Provisioning Document Generator
    Implements EP01: Monitoring Infrastructure and EP02: Custom Filtering
    """

    def __init__(self, config: GrafanaConfig):
        self.config = config
        self.provisioning_dir = Path("provisioning")
        self.dashboards_dir = Path("dashboards")

    def generate_all(self) -> None:
        """
        Generate all provisioning docs - US01: Painéis prontos
        """
        self._create_directories()
        self.generate_datasource_config()
        self.generate_dashboard_config()
        self.generate_access_control_config()
        self.generate_grafana_ini()
        self.update_dashboard_templates()

        print(f"✅ Provisioning successfully generated at {datetime.now()}")
        print(
            f"📊 Organizations have been configured: {', '.join(self.config.organizations)}"
        )
        print(
            f"📁 Repositories have been filtered: {len(self.config.repositories)} repositories"
        )

    def _create_directories(self) -> None:
        """Create required directory structure"""
        dirs = [
            self.provisioning_dir / "datasources",
            self.provisioning_dir / "dashboards",
            self.provisioning_dir / "access-control",
            self.dashboards_dir,
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

    def generate_datasource_config(self) -> None:
        """
        Generate Github data source configuration - RF01
        """
        datasource_config = DatasourceConfig()

        config_data = {
            "apiVersion": 1,
            "datasources": [
                {
                    "name": datasource_config.name,
                    "type": datasource_config.type,
                    "access": datasource_config.access,
                    "isDefault": datasource_config.is_default,
                    "secureJsonData": {"accessToken": "${GITHUB_TOKEN}"},
                    "editable": datasource_config.editable,
                }
            ],
        }

        output_path = self.provisioning_dir / "datasources" / "datasource.yaml"
        with open(output_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        print(f"📄 Generated: {output_path}")

    def generate_dashboard_config(self) -> None:
        """
        Generate dashboard config - RF02
        """
        dashboard_config = DashboardConfig()

        config_data = {
            "apiVersion": 1,
            "providers": [
                {
                    "name": dashboard_config.provider_name,
                    "orgId": dashboard_config.org_id,
                    "folder": dashboard_config.folder,
                    "type": dashboard_config.type,
                    "disableDeletion": dashboard_config.disable_deletion,
                    "updateIntervalSeconds": dashboard_config.update_interval_seconds,
                    "allowUiUpdates": dashboard_config.allow_ui_updates,
                    "options": {
                        "path": dashboard_config.path,
                        "foldersFromFilesStructure": True,
                    },
                }
            ],
        }

        output_path = self.provisioning_dir / "dashboards" / "dashboard.yaml"
        with open(output_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        print(f"📄 Gerado: {output_path}")

    def generate_access_control_config(self) -> None:
        """
        Generate access control config - RF03
        """
        access_config = AccessControlConfig()

        config_data = {
            "apiVersion": 1,
            "roles": [
                {
                    "name": access_config.role_name,
                    "description": access_config.description,
                    "permissions": [
                        {"action": "dashboards:read", "scope": "dashboards:*"},
                        {"action": "datasources:read", "scope": "datasources:*"},
                    ],
                }
            ],
            "assignments": [
                {
                    "name": access_config.assignment_name,
                    "role": access_config.role_name,
                    "target": access_config.target,
                }
            ],
        }

        output_path = self.provisioning_dir / "access-control" / "api-permissions.yaml"
        with open(output_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        print(f"📄 Generated: {output_path}")

    def generate_grafana_ini(self) -> None:
        """
        Generate main Grafana config - US02
        """
        ini_content = f"""[paths]
provisioning = /etc/grafana/provisioning

[server]
root_url = {self.config.server_root_url}
domain = {self.config.server_domain}
enforce_domain = {str(self.config.enforce_domain).lower()}

[security]
allow_embedding = true
disable_gravatar = true
cookie_secure = true
cookie_samesite = strict
disable_initial_admin_creation = true

[auth]
disable_login_form = true 
oauth_auto_login = false

[auth.anonymous]
enabled = true
org_role = Viewer
hide_version = true

[dashboards]
default_home_dashboard_path = /var/lib/grafana/dashboards/github.json
min_refresh_interval = 1m

[analytics]
reporting_enabled = false
check_for_updates = false

[feature_toggles]
publicDashboards = false
accessTokenExpirationCheck = false
"""

        with open("grafana.ini.template", "w") as f:
            f.write(ini_content)

        print("📄 Generated: grafana.ini.template")

    def update_dashboard_templates(self) -> None:
        """
        Update dashboard templates based on specified filter - US03
        """
        repo_names = [repo.split("/")[-1] for repo in self.config.repositories]
        repo_regex = f"^({'|'.join(repo_names)})$"

        org_options = []
        for i, org in enumerate(self.config.organizations):
            org_options.append(
                {
                    "selected": i == 0,
                    "text": org,
                    "value": org,
                }
            )

        dashboard_updates = {
            "repo_regex": repo_regex,
            "org_options": org_options,
            "default_org": self.config.organizations[0]
            if self.config.organizations
            else "docker",
            "org_list": ",".join(self.config.organizations),
        }

        with open("dashboard_config.json", "w") as f:
            json.dump(dashboard_updates, f, indent=2)

        print("📄 Generated: dashboard_config.json")
        print(f"🔍 Repository regex: {repo_regex}")
        print(f"🏢 Orgs: {dashboard_updates['org_list']}")


def load_config_from_env() -> GrafanaConfig:
    """
    Loads Configuration from .env and env vars
    """
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value.strip("\"'")

    github_token = os.getenv("GITHUB_TOKEN", "")
    repos_str = os.getenv("REPOS", "")

    if not github_token:
        raise ValueError("GITHUB_TOKEN is required")

    if not repos_str:
        raise ValueError("REPOS env var is required (format: 'org1/repo1, org2/repo2')")

    repositories = [repo.strip() for repo in repos_str.split(",")]
    organizations = list(set(repo.split("/")[0] for repo in repositories))

    return GrafanaConfig(
        github_token=github_token,
        organizations=organizations,
        repositories=repositories,
        server_root_url=os.getenv("GF_SERVER_ROOT_URL", "http://localhost:3000"),
        server_domain=os.getenv("GF_SERVER_DOMAIN", "localhost"),
        enforce_domain=os.getenv("GF_SERVER_ENFORCE_DOMAIN", "true").lower() == "true",
    )


def main():
    try:
        print("🚀  Initializing Grafana provisioning...")

        config = load_config_from_env()

        generator = GrafanaProvisioningGenerator(config)
        generator.generate_all()

        print("\n✨ Generation has succeeded!")
        print("💡 Now execute 'docker-compose up -d' to apply configs")

    except Exception as e:
        print(f"❌ Error generating: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
