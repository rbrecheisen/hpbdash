#!/bin/bash

# activate virtualenv
source ~/.venv/hpbdash/bin/activate

# run server
echo "running prefect server..."
prefect server start &

# run agent
echo "running agent..."
prefect agent start -p 'default-agent-pool' -q 'test' &

# run webapp
echo "running dashboard..."
./init_app.sh &
