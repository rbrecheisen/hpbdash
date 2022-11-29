#!/bin/bash
cp ../src/airflow/* ./dags
docker-compose up -d --force-recreate && docker-compose logs -f
