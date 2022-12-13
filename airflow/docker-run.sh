#!/bin/bash
cd ..
git pull
cp src/airflow/* airflow/dags
cd airflow
docker-compose up -d --force-recreate && docker-compose logs -f
