import os
import logging
import datetime

from prefect import flow, task
from barbell2.castor.api import CastorApiClient


STUDY = 'ESPRESSO_v2.0_DPCA'
CLIENT_ID = open(os.path.join(os.environ['HOME'], 'castorclientid.txt'), 'r').readline().strip()
CLIENT_SECRET = open(os.path.join(os.environ['HOME'], 'castorclientsecret.txt'), 'r').readline().strip()
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@task(name='extract_data', retries=2, retry_delay_seconds=2)
def extract_data():
    """ 
    Uses Castor API to extract record and field data. 
    """
    raise RuntimeError()
    client = CastorApiClient(CLIENT_ID, CLIENT_SECRET)
    study = client.get_study(STUDY)
    print(study)


@flow(name='castor2sqlite')
def castor2sqlite():
    """ 
    Extracts Castor data and builds queryable SQL database from this data.
    """
    extract_data()


if __name__ == '__main__':
    castor2sqlite()
