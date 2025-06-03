# Makefile for GitHub Grafana Dashboard Automation

.PHONY: help setup install generate update start stop clean status logs test validate

PYTHON := python3
COMPOSE := docker-compose
VENV := venv

RED := $(shell tput setaf 1)
GREEN := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
BLUE := $(shell tput setaf 4)
PURPLE := $(shell tput setaf 5)
CYAN := $(shell tput setaf 6)
NC := $(shell tput sgr0) # No Color

help:
	@echo "$(CYAN)🚀 Dashboard GitHub Grafana - Automation$(NC)"
	@echo "$(CYAN)Implements requirements RF01, RF02, RF03$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-15s$(NC) %s\n", $$1, $$2}'

install:
	@echo "$(YELLOW)📦 Installing deps...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies were installed$(NC)"

setup: install
	@echo "$(PURPLE)🔧 Initializing configuration wizard...$(NC)"
	$(PYTHON) interactive_setup.py
	@echo "$(GREEN)✅ Configuration was complete$(NC)"

generate:
	@echo "$(YELLOW)⚙️  Generating provisioning files...$(NC)"
	$(PYTHON) generate_provisioning.py
	@echo "$(GREEN)✅ Provisioning was generated$(NC)"

update:
	@echo "$(YELLOW)🔄 Updating dashboards...$(NC)"
	$(PYTHON) update_dashboards.py
	@echo "$(GREEN)✅ Dashboards were updated$(NC)"

validate:
	@echo "$(YELLOW)✅ Validating config...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ .env file not found. Execute 'make setup'$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f provisioning/datasources/datasource.yaml ]; then \
		echo "$(RED)❌ Provisioning files not found. Execute 'make generate'$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ Valid config$(NC)"

build: validate
	@echo "$(YELLOW)🏗️  Building images...$(NC)"
	$(COMPOSE) build
	@echo "$(GREEN)✅ Images were built$(NC)"

start: validate
	@echo "$(YELLOW)🚀 Initializing dashboard...$(NC)"
	$(COMPOSE) up -d
	@echo "$(GREEN)✅ Dashboard has started$(NC)"
	@echo "$(CYAN)🌐 Acess: http://localhost:3000$(NC)"

stop:
	@echo "$(YELLOW)⏹️  Stopping dashboard...$(NC)"
	$(COMPOSE) down
	@echo "$(GREEN)✅ Dashboard has stopped$(NC)"

restart: stop start

status:
	@echo "$(CYAN)📊 Containers status:$(NC)"
	$(COMPOSE) ps

logs:
	@echo "$(CYAN)📜 Grafana logs:$(NC)"
	$(COMPOSE) logs -f grafana

test:
	@echo "$(YELLOW)🧪 Running tests...$(NC)"
	@chmod +x test/*.sh
	@./test/validate-config.sh
	@if $(COMPOSE) ps | grep -q grafana; then \
		./test/integration-test.sh; \
	else \
		echo "$(YELLOW)⚠️  Grafana is not running. Execute 'make start'$(NC)"; \
	fi
	@echo "$(GREEN)✅ Tests have finished$(NC)"

clean:
	@echo "$(YELLOW)🧹 Cleaning temporary files...$(NC)"
	rm -f dashboard_config.json
	rm -f grafana.ini
	rm -rf __pycache__
	rm -rf *.pyc
	$(COMPOSE) down -v --remove-orphans
	@echo "$(GREEN)✅ Cleaning has completed$(NC)"

reset: clean
	@echo "$(RED)⚠️  WARNING: This will remove all files related to Grafana! \(grafana-data/\)$(NC)"
	@read -p "Are you sure? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(YELLOW)🔄 Removing data...$(NC)"
	sudo rm -rf grafana-data/
	rm -f .env
	@echo "$(GREEN)✅ Reset has concluded$(NC)"

quick-start: setup generate update start
	@echo "$(GREEN)🎉 Quick start has concluded!$(NC)"
	@echo "$(CYAN)🌐 Dashboard available at: http://localhost:3000$(NC)"

dev-setup:
	@echo "$(YELLOW)🛠️  Configuring dev environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✅ venv created at: $(VENV)/$(NC)"
	@echo "$(CYAN)💡 activate it with: \'source $(VENV)/bin/activate$(NC)\'"

lint:
	@echo "$(YELLOW)🔍 Verifying code...$(NC)"
	@which flake8 >/dev/null 2>&1 || (echo "$(RED)❌ flake8 not found$(NC)" && exit 1)
	flake8 *.py --max-line-length=100 --ignore=E501
	@echo "$(GREEN)✅ Code has been verified$(NC)"

info:
	@echo "$(CYAN)ℹ️  System info:$(NC)"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Docker: $$(docker --version)"
	@echo "Docker Compose: $$($(COMPOSE) --version)"
	@if [ -f .env ]; then \
		echo "Config: ✅ Present"; \
		echo "Orgs: $$(grep REPOS .env | cut -d'=' -f2 | tr ',' '\n' | cut -d'/' -f1 | sort -u | tr '\n' ' ')"; \
	else \
		echo "Config missing. (execute 'make setup')"; \
	fi

backup:
	@echo "$(YELLOW)💾 Creating backup...$(NC)"
	@mkdir -p backups
	@tar -czf backups/grafana-config-$$(date +%Y%m%d-%H%M%S).tar.gz \
		.env provisioning/ dashboards/ grafana.ini.template 2>/dev/null || true
	@echo "$(GREEN)✅ Backup has been created at backups/$(NC)"
