import os
import logging

from prefect import flow, task
from castor import CastorToJson, CastorJsonToDataFrame


STUDY_DPCA = 'ESPRESSO_v2.0_DPCA'
STUDY_DHBA = 'ESPRESSO_v2.0_DHBA'
CLIENT_ID_FILE = os.path.join(os.environ['HOME'], 'castorclientid.txt')
CLIENT_ID = open(CLIENT_ID_FILE, 'r').readline().strip()
CLIENT_SECRET_FILE = os.path.join(os.environ['HOME'], 'castorclientsecret.txt')
CLIENT_SECRET = open(CLIENT_SECRET_FILE, 'r').readline().strip()
OUTPUT_JSON_FILE_DPCA = '/tmp/castor/dpca.json'
OUTPUT_JSON_FILE_DHBA = '/tmp/castor/dhba.json'

if not os.path.isfile(CLIENT_ID_FILE):
    raise RuntimeError(f'Castor client ID file {CLIENT_ID_FILE} does not exist!')
if not os.path.isfile(CLIENT_SECRET_FILE):
    raise RuntimeError(f'Castor client secret file {CLIENT_SECRET_FILE} does not exist!')
if not os.path.isdir('/tmp/castor'):
    os.makedirs('/tmp/castor')

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@task(name='extract_dhba')
def extract_dhba():
    extractor = CastorToJson(STUDY_DHBA, CLIENT_ID, CLIENT_SECRET, OUTPUT_JSON_FILE_DHBA)
    extractor.execute()


@task(name='extract_dpca')
def extract_dpca():
    extractor = CastorToJson(STUDY_DPCA, CLIENT_ID, CLIENT_SECRET, OUTPUT_JSON_FILE_DPCA)
    output_json = extractor.execute()
    to_df = CastorJsonToDataFrame(output_json)
    df = to_df.execute()
    df.to_csv('dpca.csv')


@flow(name='castor2json')
def castor2json():
    # extract_dhba()
    extract_dpca()


if __name__ == '__main__':
    castor2json()
