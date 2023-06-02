#!/bin/bash

echo "deleting deployment..."
# prefect deployment delete castor2sqlite/castor2sqlite
prefect deployment delete castor2csv/castor2csv

echo "killing prefect processes..."
for pid in $(ps -ef|grep "prefect"|awk '{print $2}'); do
    kill -9 $pid &>/dev/null
done
