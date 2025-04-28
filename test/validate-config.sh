#!/bin/bash
set -e

# Get the root directory of the project
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Validate .env file
if [ ! -f "${ROOT_DIR}/.env" ]; then
  echo "Error: .env file not found"
  exit 1
fi

# Change to root directory before running docker-compose
cd "${ROOT_DIR}"

# Validate docker-compose.yml
if ! docker compose config -q; then
  echo "Error: docker-compose.yml validation failed"
  exit 1
fi

# Validate dashboard JSON
if ! jq . "${ROOT_DIR}/dashboards/github.json" >/dev/null 2>&1; then
  echo "Error: Invalid dashboard JSON"
  exit 1
fi

# Validate Grafana provisioning
if [ ! -d "${ROOT_DIR}/provisioning" ] || [ ! -f "${ROOT_DIR}/provisioning/datasources/datasource.yaml" ]; then
  echo "Error: Missing provisioning configuration"
  exit 1
fi

echo "All configurations valid!"
exit 0