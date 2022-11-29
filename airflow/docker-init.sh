#!/bin/bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env  # IMPORTANT! Without this environment variable, it doesn't work!
docker-compose up airflow-init
