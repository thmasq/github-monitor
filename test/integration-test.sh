#!/bin/bash
set -e

# Test Grafana API health
echo "Testing Grafana API health..."
response=$(curl -s http://localhost:3000/api/health)
if [[ $response != *"ok"* ]]; then
  echo "Grafana health check failed"
  exit 1
fi
echo "Grafana API health check passed"

# Test if GitHub datasource is configured
echo "Testing GitHub datasource configuration..."
response=$(curl -s http://localhost:3000/api/datasources)
if [[ $response != *"grafana-github-datasource"* ]]; then
  echo "GitHub datasource not found"
  exit 1
fi
echo "GitHub datasource configuration passed"

# Add new tests 

echo "All tests passed!"
exit 0