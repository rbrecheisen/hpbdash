#!/bin/bash

echo "running prefect server..."
prefect server start &

echo "running agent..."
prefect agent start -p 'default-agent-pool' -q 'test' &

echo "running dashboard..."
./run_app.sh

echo "killing prefect processes..."
for pid in $(ps -ef|grep "prefect"|awk '{print $2}'); do
    kill -9 $pid 2>&1 /dev/null
done
