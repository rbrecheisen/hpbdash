#!/bin/bash
docker-compose down --volumes --remove-orphans
rm -rf ./dags
rm -rf ./logs
rm -rf ./plugins
