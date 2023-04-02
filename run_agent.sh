#!/bin/bash

export PREFECT_LOCAL_STORAGE=/Users/ralph/dev/hpbdash/src/prefect/deployments/castor2sqlite

prefect agent start -p 'default-agent-pool' -q 'test'
