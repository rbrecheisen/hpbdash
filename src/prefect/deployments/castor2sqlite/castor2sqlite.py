import os
import logging

from prefect import flow, task
from barbell2_castor import CastorToSqlite3


STUDY_DPCA = 'ESPRESSO_v2.0_DPCA'
STUDY_DHBA = 'ESPRESSO_v2.0_DHBA'
CLIENT_ID_FILE = os.path.join(os.environ['HOME'], 'castorclientid.txt')
if not os.path.isfile(CLIENT_ID_FILE):
    raise RuntimeError(f'Castor client ID file {CLIENT_ID_FILE} does not exist!')
CLIENT_ID = open(CLIENT_ID_FILE, 'r').readline().strip()
CLIENT_SECRET_FILE = os.path.join(os.environ['HOME'], 'castorclientsecret.txt')
if not os.path.isfile(CLIENT_SECRET_FILE):
    raise RuntimeError(f'Castor client secret file {CLIENT_SECRET_FILE} does not exist!')
CLIENT_SECRET = open(CLIENT_SECRET_FILE, 'r').readline().strip()
OUTPUT_DB_FILE_DPCA = '/tmp/castor/dpca.db'
OUTPUT_DB_FILE_DHBA = '/tmp/castor/dhba.db'
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@task(name='extract_dpca')
def extract_dpca():
    extractor = CastorToSqlite3(
        STUDY_DPCA, 
        CLIENT_ID, 
        CLIENT_SECRET, 
        output_db_file=OUTPUT_DB_FILE_DPCA,
        add_timestamp=False,
    )
    extractor.execute()


@task(name='extract_dhba')
def extract_dhba():
    extractor = CastorToSqlite3(
        STUDY_DHBA, 
        CLIENT_ID, 
        CLIENT_SECRET, 
        output_db_file=OUTPUT_DB_FILE_DHBA,
        add_timestamp=False,
    )
    extractor.execute()


@flow(name='castor2sqlite')
def castor2sqlite():
    extract_dpca()
    extract_dhba()


if __name__ == '__main__':
    castor2sqlite()
