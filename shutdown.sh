#!/bin/bash

echo "killing prefect processes..."
for pid in $(ps -ef|grep "prefect"|awk '{print $2}'); do
    kill -9 $pid &>/dev/null
done
