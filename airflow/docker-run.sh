#!/bin/bash
git pull
cp ../src/airflow/* ./dags
cd ../db
docker-compose up -d --force-recreate
cd ../airflow
docker-compose up -d --force-recreate && docker-compose logs -f
