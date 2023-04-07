#!/bin/bash

server_id=$(ps -ef|grep "prefect server start"|awk 'NR==1{print $2}')
server_uvicorn_id=$(ps -ef|grep "uvicorn"|awk 'NR==1{print $2}')
agent_id=$(ps -ef|grep "prefect agent start"|awk 'NR==1{print $2}')
app_id=$(ps -ef|grep "manage.py runserver"|awk 'NR==1{print $2}')

echo "killing server processes..."
kill -9 $server_uvicorn_id
kill -9 $server_id
kill -9 $agent_id

echo "killing dashboard processes..."
ids=""
for pid in $(ps -ef|grep "manage.py runserver"|awk '{print $2}'); do
    ids="$ids $pid"
done

kill -9 $ids
