import os
import logging

from prefect import flow, task

STUDY_NAME = 'ESPRESSO_v2.0_DPCA'
CLIENT_ID = open(os.path.join(os.environ['HOME'], 'castorclientid.txt'), 'r').readline().strip()
CLIENT_SECRET = open(os.path.join(os.environ['HOME'], 'castorclientsecret.txt'), 'r').readline().strip()
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@task(name='extract_data')
def extract_data():
    pass


@flow(name='castor2sqlite')
def castor2sqlite():
    extract_data()


castor2sqlite()