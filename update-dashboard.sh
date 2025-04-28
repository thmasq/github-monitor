#!/bin/bash

# Exit on error
set -e

source .env

# Default values
DASHBOARD_FILE="dashboards/github.json"

# Check if REPOS is set
if [ -z "${REPOS}" ]; then
  echo "Error: REPOS environment variable not set"
  echo "Example: REPOS=\"YaLTeR/niri, YaLTeR/wl-clipboard-rs, hyperlight-dev/hyperlight, docker/buildx, docker/model-cli\""
  exit 1
fi

echo "Processing repositories: ${REPOS}"

# Clean and parse the repos
REPOS_CLEAN=$(echo "${REPOS}" | tr -d ' ')
IFS=',' read -ra REPO_ARRAY <<< "${REPOS_CLEAN}"

# Extract unique organizations
ORGS=()
REPO_NAMES=()
for repo in "${REPO_ARRAY[@]}"; do
  ORG=$(echo "${repo}" | cut -d'/' -f1)
  REPO_NAME=$(echo "${repo}" | cut -d'/' -f2)
  
  ORGS+=("${ORG}")
  REPO_NAMES+=("${REPO_NAME}")
done

# Get unique organizations
UNIQUE_ORGS=($(echo "${ORGS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))
ORG_LIST=$(IFS=','; echo "${UNIQUE_ORGS[*]}")

# Create regex pattern for repository names
REPO_PATTERN=$(IFS='|'; echo "${REPO_NAMES[*]}")
REPO_REGEX="^(${REPO_PATTERN})\$"

echo "Organizations: ${ORG_LIST}"
echo "Repository regex: ${REPO_REGEX}"

# Create org options JSON for dashboard
ORG_OPTIONS="["
for i in "${!UNIQUE_ORGS[@]}"; do
  SELECTED="false"
  if [ $i -eq 0 ]; then
    SELECTED="true"
  fi
  ORG_OPTIONS+="{ \"selected\": ${SELECTED}, \"text\": \"${UNIQUE_ORGS[$i]}\", \"value\": \"${UNIQUE_ORGS[$i]}\" }"
  if [ $i -lt $((${#UNIQUE_ORGS[@]} - 1)) ]; then
    ORG_OPTIONS+=","
  fi
done
ORG_OPTIONS+="]"

# First organization to use as default
DEFAULT_ORG="${UNIQUE_ORGS[0]}"

# Update dashboard JSON with jq
TMP_FILE=$(mktemp)
jq --arg orgs "${ORG_LIST}" \
   --arg regex "${REPO_REGEX}" \
   --argjson options "${ORG_OPTIONS}" \
   --arg default_org "${DEFAULT_ORG}" \
   '.templating.list |= map(
      if .name == "organization" then
        .options = $options |
        .query = $orgs |
        .current.text = $default_org |
        .current.value = $default_org
      elif .name == "repository" then
        .regex = $regex
      else .
      end
    )' "${DASHBOARD_FILE}" > "${TMP_FILE}"

# Check if jq command succeeded
if [ $? -eq 0 ]; then
  mv "${TMP_FILE}" "${DASHBOARD_FILE}"
  echo "Successfully updated dashboard with repository filter"
  echo "Organizations: ${ORG_LIST}"
  echo "Repository regex: ${REPO_REGEX}"
else
  rm "${TMP_FILE}"
  echo "Error updating dashboard file"
  exit 1
fi
