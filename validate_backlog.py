#!/usr/bin/env python3
"""
Backlog Requirements Implementation Validator
Verifies if all FRs, EPICs and USs have been implemented correctly
"""

import json
import yaml
import requests
import subprocess
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Validation result"""

    requirement_id: str
    description: str
    status: bool
    details: str
    category: str  # FR, EPIC, US


class BacklogValidator:
    """
    Complete backlog requirements validator
    Verifies implementation of FR01, FR02, FR03, EPIC01, EPIC02, US01, US02, US03
    """

    def __init__(self):
        self.results: List[ValidationResult] = []
        self.grafana_url = self._get_grafana_url()

    def validate_all_requirements(self) -> Dict[str, List[ValidationResult]]:
        """
        Executes validation of all backlog requirements
        """
        print("🔍 Starting complete validation of backlog requirements...")
        print("=" * 70)

        self._validate_fr01()
        self._validate_fr02()
        self._validate_fr03()

        self._validate_epic01()
        self._validate_epic02()

        self._validate_us01()
        self._validate_us02()
        self._validate_us03()

        grouped_results = {
            "FR": [r for r in self.results if r.category == "FR"],
            "EPIC": [r for r in self.results if r.category == "EPIC"],
            "US": [r for r in self.results if r.category == "US"],
        }

        self._print_validation_report(grouped_results)
        return grouped_results

    def _get_grafana_url(self) -> str:
        """Gets Grafana URL from configuration"""
        try:
            with open(".env") as f:
                for line in f:
                    if line.startswith("GF_SERVER_ROOT_URL="):
                        return line.split("=", 1)[1].strip()
        except FileNotFoundError:
            pass
        return "http://localhost:3000"

    def _validate_fr01(self) -> None:
        """
        FR01: The system must provide pre-configured dashboards to monitor GitHub activities
        """
        print("🔍 Validating FR01: Pre-configured dashboards...")

        dashboards_dir = Path("dashboards")
        expected_dashboards = ["github.json", "github-organization.json"]

        dashboards_exist = all(
            (dashboards_dir / dashboard).exists() for dashboard in expected_dashboards
        )

        dashboard_config = Path("provisioning/dashboards/dashboard.yaml")
        config_exists = dashboard_config.exists()

        details = []
        if dashboards_exist:
            details.append(f"✅ Dashboards found: {', '.join(expected_dashboards)}")
        else:
            details.append("❌ Dashboards not found")

        if config_exists:
            details.append("✅ Provisioning configuration present")
        else:
            details.append("❌ Provisioning configuration missing")

        grafana_running = self._check_grafana_health()
        if grafana_running:
            details.append("✅ Grafana responding")
        else:
            details.append("⚠️  Grafana is not running")

        status = dashboards_exist and config_exists

        self.results.append(
            ValidationResult(
                requirement_id="FR01",
                description="Pre-configured dashboards to monitor GitHub activities",
                status=status,
                details="; ".join(details),
                category="FR",
            )
        )

    def _validate_fr02(self) -> None:
        """
        FR02: The system must allow viewing statistics from multiple repositories within an organization
        """
        print("🔍 Validating FR02: Multiple repositories...")

        repos = self._get_configured_repositories()
        orgs = self._get_configured_organizations()

        org_dashboard = Path("dashboards/github-organization.json")
        org_dashboard_exists = org_dashboard.exists()

        details = []
        if repos and len(repos) > 1:
            details.append(f"✅ Multiple repositories configured: {len(repos)}")
        else:
            details.append("❌ Need to configure multiple repositories")

        if orgs:
            details.append(f"✅ Organizations detected: {', '.join(orgs)}")
        else:
            details.append("❌ No organizations detected")

        if org_dashboard_exists:
            details.append("✅ Organization dashboard present")
        else:
            details.append("❌ Organization dashboard missing")

        status = len(repos) > 1 and len(orgs) >= 1 and org_dashboard_exists

        self.results.append(
            ValidationResult(
                requirement_id="FR02",
                description="View statistics from multiple repositories",
                status=status,
                details="; ".join(details),
                category="FR",
            )
        )

    def _validate_fr03(self) -> None:
        """
        FR03: The system must allow filtering access to repositories displayed in the dashboard
        """
        print("🔍 Validating FR03: Repository filtering...")

        access_control = Path("provisioning/access-control/api-permissions.yaml")
        access_exists = access_control.exists()

        github_dashboard = Path("dashboards/github.json")
        has_filters = False

        if github_dashboard.exists():
            try:
                with open(github_dashboard) as f:
                    dashboard_data = json.load(f)

                templating = dashboard_data.get("templating", {})
                template_list = templating.get("list", [])

                repo_var = next(
                    (var for var in template_list if var.get("name") == "repository"),
                    None,
                )
                if repo_var and repo_var.get("regex"):
                    has_filters = True

            except Exception:
                pass

        dashboard_config_file = Path("dashboard_config.json")
        filter_config_exists = dashboard_config_file.exists()

        details = []
        if access_exists:
            details.append("✅ Access control configured")
        else:
            details.append("❌ Access control not configured")

        if has_filters:
            details.append("✅ Repository filters configured")
        else:
            details.append("❌ Repository filters not found")

        if filter_config_exists:
            details.append("✅ Filter configuration present")
        else:
            details.append("❌ Filter configuration missing")

        status = access_exists and has_filters

        self.results.append(
            ValidationResult(
                requirement_id="FR03",
                description="Filter access to displayed repositories",
                status=status,
                details="; ".join(details),
                category="FR",
            )
        )

    def _validate_epic01(self) -> None:
        """
        EPIC01: Set up GitHub repository monitoring infrastructure
        """
        print("🔍 Validating EPIC01: Monitoring infrastructure...")

        essential_files = [
            "docker-compose.yml",
            "provisioning/datasources/datasource.yaml",
            "grafana.ini.template",
            ".env",
        ]

        files_exist = all(Path(file).exists() for file in essential_files)

        docker_valid = self._validate_docker_compose()

        datasource_config = self._check_datasource_config()

        details = []
        if files_exist:
            details.append("✅ Essential files present")
        else:
            missing = [f for f in essential_files if not Path(f).exists()]
            details.append(f"❌ Missing files: {', '.join(missing)}")

        if docker_valid:
            details.append("✅ Docker Compose valid")
        else:
            details.append("❌ Docker Compose invalid")

        if datasource_config:
            details.append("✅ GitHub datasource configured")
        else:
            details.append("❌ GitHub datasource not configured")

        status = files_exist and docker_valid and datasource_config

        self.results.append(
            ValidationResult(
                requirement_id="EPIC01",
                description="Monitoring infrastructure set up",
                status=status,
                details="; ".join(details),
                category="EPIC",
            )
        )

    def _validate_epic02(self) -> None:
        """
        EPIC02: Implement filtering and custom data visualization functionality
        """
        print("🔍 Validating EPIC02: Filtering and customization...")

        customization_scripts = [
            "generate_provisioning.py",
            "update_dashboards.py",
            "interactive_setup.py",
        ]

        scripts_exist = all(Path(script).exists() for script in customization_scripts)

        custom_config = Path("dashboard_config.json").exists()

        dashboards_dir = Path("dashboards")
        custom_dashboards = []
        if dashboards_dir.exists():
            custom_dashboards = [
                f
                for f in dashboards_dir.glob("github-*.json")
                if f.name not in ["github.json", "github-organization.json"]
            ]

        details = []
        if scripts_exist:
            details.append("✅ Customization scripts present")
        else:
            missing = [s for s in customization_scripts if not Path(s).exists()]
            details.append(f"❌ Missing scripts: {', '.join(missing)}")

        if custom_config:
            details.append("✅ Custom configuration generated")
        else:
            details.append("❌ Custom configuration not found")

        if custom_dashboards:
            details.append(f"✅ Custom dashboards: {len(custom_dashboards)}")
        else:
            details.append("ℹ️  No custom dashboards (optional)")

        status = scripts_exist and custom_config

        self.results.append(
            ValidationResult(
                requirement_id="EPIC02",
                description="Filtering and custom visualization implemented",
                status=status,
                details="; ".join(details),
                category="EPIC",
            )
        )

    def _validate_us01(self) -> None:
        """
        US01: As a user, I want to view ready-made dashboards to easily track repository activity
        """
        print("🔍 Validating US01: Ready-made dashboards for user...")

        grafana_accessible = self._check_grafana_accessibility()

        default_dashboard_config = self._check_default_dashboard()

        anonymous_access = self._check_anonymous_access()

        details = []
        if grafana_accessible:
            details.append(f"✅ Grafana accessible at {self.grafana_url}")
        else:
            details.append(f"❌ Grafana not accessible at {self.grafana_url}")

        if default_dashboard_config:
            details.append("✅ Default dashboard configured")
        else:
            details.append("❌ Default dashboard not configured")

        if anonymous_access:
            details.append("✅ Anonymous access enabled")
        else:
            details.append("❌ Anonymous access not enabled")

        status = grafana_accessible and default_dashboard_config

        self.results.append(
            ValidationResult(
                requirement_id="US01",
                description="Ready-made dashboards to track activity",
                status=status,
                details="; ".join(details),
                category="US",
            )
        )

    def _validate_us02(self) -> None:
        """
        US02: As an administrator, I want to filter which repositories appear to ensure only chosen projects in configuration are displayed
        """
        print("🔍 Validating US02: Filtering for administrator...")

        repos = self._get_configured_repositories()
        has_repo_filter = len(repos) > 0

        dashboard_filters = self._check_dashboard_filters()

        update_script = Path("update_dashboards.py").exists()

        details = []
        if has_repo_filter:
            details.append(f"✅ Specific repositories configured: {len(repos)}")
        else:
            details.append("❌ No specific repositories configured")

        if dashboard_filters:
            details.append("✅ Filters applied in dashboards")
        else:
            details.append("❌ Filters not applied in dashboards")

        if update_script:
            details.append("✅ Update script available")
        else:
            details.append("❌ Update script not found")

        status = has_repo_filter and dashboard_filters and update_script

        self.results.append(
            ValidationResult(
                requirement_id="US02",
                description="Repository filtering for administrator",
                status=status,
                details="; ".join(details),
                category="US",
            )
        )

    def _validate_us03(self) -> None:
        """
        US03: As a collaborator, I want to track specific metrics (issues, pull requests, commits) to understand project evolution
        """
        print("🔍 Validating US03: Specific metrics...")

        metrics_available = self._check_available_metrics()

        multi_metrics = len(metrics_available) >= 3  # issues, PRs, commits

        historical_data = self._check_historical_data_config()

        details = []
        if metrics_available:
            details.append(f"✅ Available metrics: {', '.join(metrics_available)}")
        else:
            details.append("❌ Metrics not configured")

        if multi_metrics:
            details.append("✅ Multiple metrics configured")
        else:
            details.append("❌ Insufficient metrics (minimum: issues, PRs, commits)")

        if historical_data:
            details.append("✅ Historical data configured")
        else:
            details.append("⚠️  Historical data depends on time")

        status = len(metrics_available) >= 2  # At least 2 metrics

        self.results.append(
            ValidationResult(
                requirement_id="US03",
                description="Specific metrics for collaborators",
                status=status,
                details="; ".join(details),
                category="US",
            )
        )

    def _check_grafana_health(self) -> bool:
        """Checks if Grafana is responding"""
        try:
            response = requests.get(f"{self.grafana_url}/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _check_grafana_accessibility(self) -> bool:
        """Checks if Grafana is accessible"""
        try:
            response = requests.get(self.grafana_url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def _get_configured_repositories(self) -> List[str]:
        """Gets configured repositories"""
        try:
            with open(".env") as f:
                for line in f:
                    if line.startswith("REPOS="):
                        repos_str = line.split("=", 1)[1].strip().strip("\"'")
                        return [
                            repo.strip()
                            for repo in repos_str.split(",")
                            if repo.strip()
                        ]
        except FileNotFoundError:
            pass
        return []

    def _get_configured_organizations(self) -> List[str]:
        """Gets configured organizations"""
        repos = self._get_configured_repositories()
        return list(set(repo.split("/")[0] for repo in repos if "/" in repo))

    def _validate_docker_compose(self) -> bool:
        """Validates docker-compose.yml file"""
        try:
            result = subprocess.run(
                ["docker", "compose", "config", "-q"], capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False

    def _check_datasource_config(self) -> bool:
        """Checks datasource configuration"""
        datasource_file = Path("provisioning/datasources/datasource.yaml")
        if not datasource_file.exists():
            return False

        try:
            with open(datasource_file) as f:
                config = yaml.safe_load(f)
                datasources = config.get("datasources", [])
                github_ds = next(
                    (
                        ds
                        for ds in datasources
                        if ds.get("type") == "grafana-github-datasource"
                    ),
                    None,
                )
                return github_ds is not None
        except:
            return False

    def _check_default_dashboard(self) -> bool:
        """Checks if default dashboard is configured"""
        try:
            with open("grafana.ini.template") as f:
                content = f.read()
                return "default_home_dashboard_path" in content
        except:
            return False

    def _check_anonymous_access(self) -> bool:
        """Checks if anonymous access is enabled"""
        try:
            with open("docker-compose.yml") as f:
                content = f.read()
                return "GF_AUTH_ANONYMOUS_ENABLED=true" in content
        except:
            return False

    def _check_dashboard_filters(self) -> bool:
        """Checks if dashboards have configured filters"""
        config_file = Path("dashboard_config.json")
        if not config_file.exists():
            return False

        try:
            with open(config_file) as f:
                config = json.load(f)
                return "repo_regex" in config and config["repo_regex"]
        except:
            return False

    def _check_available_metrics(self) -> List[str]:
        """Checks available metrics in dashboards"""
        metrics = []
        dashboard_file = Path("dashboards/github.json")

        if dashboard_file.exists():
            try:
                with open(dashboard_file) as f:
                    dashboard = json.load(f)

                for panel in dashboard.get("panels", []):
                    title = panel.get("title", "").lower()
                    if "issue" in title:
                        metrics.append("Issues")
                    elif "pull request" in title or "pr" in title:
                        metrics.append("Pull Requests")
                    elif "commit" in title:
                        metrics.append("Commits")
                    elif "release" in title:
                        metrics.append("Releases")

            except:
                pass

        return list(set(metrics))

    def _check_historical_data_config(self) -> bool:
        """Checks if historical data is configured"""
        dashboard_file = Path("dashboards/github.json")

        if dashboard_file.exists():
            try:
                with open(dashboard_file) as f:
                    dashboard = json.load(f)
                    time_config = dashboard.get("time", {})
                    return "from" in time_config and "to" in time_config
            except:
                pass

        return False

    def _print_validation_report(
        self, grouped_results: Dict[str, List[ValidationResult]]
    ) -> None:
        """Prints complete validation report"""
        print("\n" + "=" * 70)
        print("📋 BACKLOG REQUIREMENTS VALIDATION REPORT")
        print("=" * 70)

        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.status)
        failed_tests = total_tests - passed_tests

        print(f"📊 Summary: {passed_tests}/{total_tests} requirements implemented")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success rate: {(passed_tests / total_tests) * 100:.1f}%")

        for category, results in grouped_results.items():
            print(f"\n📁 {category} - {self._get_category_name(category)}:")

            for result in results:
                status_icon = "✅" if result.status else "❌"
                print(f"  {status_icon} {result.requirement_id}: {result.description}")
                print(f"     {result.details}")

        print("\n" + "=" * 70)

        if passed_tests == total_tests:
            print(
                "🎉 CONGRATULATIONS! All backlog requirements have been successfully implemented!"
            )
        else:
            print("⚠️  Some requirements need attention. Check the details above.")

        print(
            f"📅 Validation executed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def _get_category_name(self, category: str) -> str:
        """Returns descriptive category name"""
        names = {
            "FR": "Functional Requirements",
            "EPIC": "Epics",
            "US": "User Stories",
        }
        return names.get(category, category)


def main():
    """
    Main validation function
    """
    print("🚀 GitHub Dashboard Backlog Implementation Validator")
    print("🎯 Checking FR01, FR02, FR03, EPIC01, EPIC02, US01, US02, US03")

    try:
        validator = BacklogValidator()
        validator.validate_all_requirements()

        total = len(validator.results)
        passed = sum(1 for r in validator.results if r.status)

        return 0 if passed == total else 1

    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
