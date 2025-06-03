#!/usr/bin/env python3
"""
Interactive GitHub Monitoring System Configuration
"""

import os
import re
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class SetupConfig:
    """Complete setup configuration"""

    github_token: str
    organizations: List[str]
    repositories: List[str]
    server_url: str
    server_domain: str
    enforce_domain: bool
    setup_mode: str  # 'basic', 'advanced', 'enterprise'


class InteractiveSetup:
    """
    Interactive system configuration
    """

    def __init__(self):
        self.config = None
        self.env_file = Path(".env")

    def run_setup(self) -> SetupConfig:
        """
        Executes complete interactive configuration
        """
        print("🚀 Interactive Configuration - GitHub Grafana Dashboard")
        print("=" * 60)

        setup_mode = self._choose_setup_mode()

        github_token = self._get_github_token()
        repositories = self._get_repositories()
        organizations = self._extract_organizations(repositories)

        server_config = self._get_server_config(setup_mode)

        self.config = SetupConfig(
            github_token=github_token,
            organizations=organizations,
            repositories=repositories,
            server_url=server_config["url"],
            server_domain=server_config["domain"],
            enforce_domain=server_config["enforce_domain"],
            setup_mode=setup_mode,
        )

        self._save_env_file()

        self._show_summary()

        return self.config

    def _choose_setup_mode(self) -> str:
        """
        Choose configuration mode
        """
        print("\n📊 Choose configuration mode:")
        print("1. 🟢 Basic      - Simple setup to get started quickly")
        print("2. 🟡 Advanced   - Custom server configurations")
        print("3. 🔴 Enterprise - Complete setup for production usage environment")

        while True:
            choice = input("\nChoose an option (1-3): ").strip()

            if choice == "1":
                return "basic"
            elif choice == "2":
                return "advanced"
            elif choice == "3":
                return "enterprise"
            else:
                print("❌ Invalid option. Choose 1, 2, or 3.")

    def _get_github_token(self) -> str:
        """
        Gets GitHub token with validation
        """
        print("\n🔑 GitHub Token Configuration")
        print("📝 You need a GitHub Personal Access Token")
        print("🔗 Create one at: https://github.com/settings/tokens")
        print("⚡ Required permissions: repo, read:org, read:user")

        existing_token = os.getenv("GITHUB_TOKEN", "")
        if existing_token:
            use_existing = (
                input(
                    f"\n✅ Token found (...{existing_token[-6:]}). Use this one? (y/N): "
                )
                .strip()
                .lower()
            )
            if use_existing in ["y", "yes", "s", "sim"]:
                return existing_token

        while True:
            token = input("\n🔐 Enter your GitHub Token: ").strip()

            if not token:
                print("❌ Token cannot be empty")
                continue

            if len(token) < 20:
                print("❌ Token too short. Check if you copied it completely.")
                continue

            # Basic format validation
            if not re.match(r"^gh[sp]_[A-Za-z0-9_]{36,}$", token) and not re.match(
                r"^[a-f0-9]{40}$", token
            ):
                print("⚠️  Token format might be incorrect, but proceeding...")

            return token

    def _get_repositories(self) -> List[str]:
        """
        Gets list of repositories to monitor
        """
        print("\n📁 Repository Configuration")
        print("📝 Enter the repositories you want to monitor")
        print("📋 Format: organization/repository (e.g: docker/buildx)")
        print("💡 You can add multiple repositories")

        repositories = []

        # Check if repositories exist in .env
        existing_repos = os.getenv("REPOS", "")
        if existing_repos:
            print(f"\n✅ Repositories found: {existing_repos}")
            use_existing = input("Use these repositories? (y/N): ").strip().lower()
            if use_existing in ["y", "yes", "s", "sim"]:
                return [repo.strip() for repo in existing_repos.split(",")]

        print("\n📋 Examples of popular repositories:")
        print("   • docker/buildx")
        print("   • microsoft/vscode")
        print("   • kubernetes/kubernetes")
        print("   • grafana/grafana")

        while True:
            repo = input(
                f"\n📁 Repository #{len(repositories) + 1} (or 'done' to finish): "
            ).strip()

            if repo.lower() in ["done", "finish", "end", ""]:
                if repositories:
                    break
                else:
                    print("❌ Add at least one repository")
                    continue

            if not self._validate_repository_format(repo):
                print("❌ Invalid format. Use: organization/repository")
                continue

            if repo in repositories:
                print("⚠️  Repository already added")
                continue

            repositories.append(repo)
            print(f"✅ Added: {repo}")

        return repositories

    def _validate_repository_format(self, repo: str) -> bool:
        """Validates repository format"""
        pattern = r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$"
        return bool(re.match(pattern, repo))

    def _extract_organizations(self, repositories: List[str]) -> List[str]:
        """
        Extracts unique organizations from repositories
        RF02: Statistics by organization
        """
        orgs = list(set(repo.split("/")[0] for repo in repositories))

        print(f"\n🏢 Organizations detected: {', '.join(orgs)}")
        return orgs

    def _get_server_config(self, setup_mode: str) -> Dict[str, any]:
        """
        Gets server configurations based on mode
        EP02: Customization according to needs
        """
        if setup_mode == "basic":
            return {
                "url": "http://localhost:3000",
                "domain": "localhost",
                "enforce_domain": True,
            }

        print(f"\n🌐 Server Configuration ({setup_mode.title()})")

        default_url = "http://localhost:3000"
        server_url = input(f"🔗 Server URL ({default_url}): ").strip() or default_url

        default_domain = (
            "localhost"
            if "localhost" in server_url
            else server_url.split("//")[1].split(":")[0]
        )
        server_domain = (
            input(f"🌍 Domain ({default_domain}): ").strip() or default_domain
        )

        enforce_domain = True
        if setup_mode == "enterprise":
            enforce_input = (
                input("🔒 Enforce domain for security? (Y/n): ").strip().lower()
            )
            enforce_domain = enforce_input not in ["n", "no", "não"]

        return {
            "url": server_url,
            "domain": server_domain,
            "enforce_domain": enforce_domain,
        }

    def _save_env_file(self) -> None:
        """
        Saves configurations to .env file
        Configuration persistence
        """
        env_content = f"""# GitHub Dashboard Grafana Configuration
# Automatically generated on {self._get_timestamp()}

# GitHub access token (required)
GITHUB_TOKEN={self.config.github_token}

# Repositories to monitor (comma separated)
REPOS="{", ".join(self.config.repositories)}"

# Grafana server configurations
GF_SERVER_ROOT_URL={self.config.server_url}
GF_SERVER_DOMAIN={self.config.server_domain}
GF_SERVER_ENFORCE_DOMAIN={str(self.config.enforce_domain).lower()}

# Security configuration
GF_AUTH_ANONYMOUS_ENABLED=true
GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
GF_AUTH_DISABLE_LOGIN_FORM=true
GF_USERS_ALLOW_SIGN_UP=false

# Configuration mode used
SETUP_MODE={self.config.setup_mode}
"""

        with open(self.env_file, "w") as f:
            f.write(env_content)

        print(f"\n💾 Configuration saved to: {self.env_file}")

    def _show_summary(self) -> None:
        """
        Shows configuration summary
        US01, US02, US03: Configuration confirmation
        """
        print("\n" + "=" * 60)
        print("📋 CONFIGURATION SUMMARY")
        print("=" * 60)
        print(f"🔧 Setup mode:        {self.config.setup_mode.title()}")
        print(f"🔑 GitHub token:      Configured (...{self.config.github_token[-6:]})")
        print(
            f"🏢 Organizations:     {len(self.config.organizations)} ({', '.join(self.config.organizations)})"
        )
        print(f"📁 Repositories:      {len(self.config.repositories)}")
        for i, repo in enumerate(self.config.repositories, 1):
            print(f"   {i:2d}. {repo}")
        print(f"🌐 Server URL:        {self.config.server_url}")
        print(f"🌍 Domain:           {self.config.server_domain}")
        print(f"🔒 Enforce domain:   {'Yes' if self.config.enforce_domain else 'No'}")
        print("=" * 60)

        print("\n🎯 NEXT STEPS:")
        print("1. Run: python3 generate_provisioning.py")
        print("2. Run: python3 update_dashboards.py")
        print("3. Run: docker-compose up -d")
        print("4. Access: " + self.config.server_url)
        print("\n✨ Setup completed successfully!")

    def _get_timestamp(self) -> str:
        """Returns current timestamp"""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """
    Main function for interactive setup
    Entry point for complete system configuration
    """
    try:
        setup = InteractiveSetup()
        setup.run_setup()

        auto_generate = (
            input("\n🤖 Generate provisioning files automatically? (Y/n): ")
            .strip()
            .lower()
        )

        if auto_generate not in ["n", "no", "não"]:
            print("\n🔄 Generating provisioning files...")

            try:
                from generate_provisioning import main as generate_main

                generate_main()

                from update_dashboards import main as update_main

                update_main()

                print("\n🎉 System configured and ready to use!")
                print("🚀 Run: docker-compose up -d")

            except ImportError:
                print("⚠️  Generation scripts not found. Run manually:")
                print("   python3 generate_provisioning.py")
                print("   python3 update_dashboards.py")

        return 0

    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user")
        return 1

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
