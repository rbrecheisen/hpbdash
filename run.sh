#!/bin/bash

./shutdown.sh

echo "updating prefect deployments..."
rm -rf ~/.prefect

# cd src/prefect/deployments/castor2sqlite
# # prefect deployment build ./castor2sqlite.py:castor2sqlite -n castor2sqlite -q test --skip-upload --cron "*/10 * * * *"
# prefect deployment build ./castor2sqlite.py:castor2sqlite -n castor2sqlite -q test --skip-upload
# prefect deployment apply ./castor2sqlite-deployment.yaml

# cd src/prefect/deployments/castor2csv
# prefect deployment build ./castor2csv.py:castor2csv -n castor2csv -q test --skip-upload
# prefect deployment apply ./castor2csv-deployment.yaml

cd src/prefect/deployments/castor2json
# prefect deployment build ./castor2json.py:castor2json -n castor2json -q test --skip-upload --cron "*/10 * * * *"
prefect deployment build ./castor2json.py:castor2json -n castor2json -q test --skip-upload
prefect deployment apply ./castor2json-deployment.yaml

echo "running prefect server..."
prefect server start &

echo "running agent..."
prefect agent start -p 'default-agent-pool' -q 'test' &

echo "running flow..."
# prefect deployment run castor2sqlite/castor2sqlite
# prefect deployment run castor2csv/castor2csv
prefect deployment run castor2json/castor2json