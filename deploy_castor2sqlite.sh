#!/bin/bash

rm -rf ~/.prefect

cd src/prefect/deployments/castor2sqlite

prefect deployment build ./castor2sqlite.py:castor2sqlite -n castor2sqlite -q test --skip-upload --cron "*/10 * * * *"
prefect deployment apply ./castor2sqlite-deployment.yaml