#!/bin/bash

cd src/prefect/deployments/castor2sqlite

prefect deployment build ./castor2sqlite.py:castor2sqlite -n castor2sqlite -q test --skip-upload