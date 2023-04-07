#!/bin/bash

echo "running prefect server..."
prefect server start &

echo "running agent..."
prefect agent start -p 'default-agent-pool' -q 'test' &