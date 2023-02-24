#!/bin/bash
mkdir -p ./dags ./logs ./plugins ./db
echo -e "AIRFLOW_UID=$(id -u)" > .env  # IMPORTANT! Without this environment variable, it doesn't work!
echo -e "CASTOR_CLIENT_ID=$(cat $HOME/castorclientid.txt)" >> .env
echo -e "CASTOR_CLIENT_SECRET=$(cat $HOME/castorclientsecret.txt)" >> .env
docker-compose up airflow-init
