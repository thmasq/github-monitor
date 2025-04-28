#!/bin/bash
# Probably not necessary for every docker setup, but definitely necessary if you're running SE Linux
mkdir -p grafana-data
chown -R 472:472 grafana-data provisioning dashboards
chmod -R 755 grafana-data provisioning dashboards
chmod 644 grafana.ini