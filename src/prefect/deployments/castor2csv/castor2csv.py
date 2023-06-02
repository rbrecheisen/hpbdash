import os
import json
import logging
import pandas as pd

from prefect import flow, task
from barbell2_castor import CastorToSqlite3
from barbell2_castor.castor2sqlite import CastorToDict


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
OUTPUT_CSV_FILE_DPCA = '/tmp/castor/dpca.csv'
OUTPUT_JSON_FILE_DPCA = '/tmp/castor/dpca.json'
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class CastorToCSV:

    def __init__(self, study_name, client_id, client_secret):
        self.study_name = study_name
        self.client_id = client_id
        self.client_secret = client_secret

    def get_dtype(field_type):
        if field_type == 'radio' or field_type == 'checkbox':
            return 'bool'
        if field_type == 'numeric':
            return 'int64'
        return 'str'
    
    def execute(self):
        castor2dict = CastorToDict(self.study_name, self.client_id, self.client_secret)
        data = castor2dict.execute()
        df_data = {}
        df_data_types = {}
        for field_name in data.keys():
            df_data[field_name] = data[field_name]['field_values']
            df_data_types[field_name].dtype = self.get_dtype(data[field_name]['field_type'])
        df = pd.DataFrame(data=df_data)
        df.to_csv(OUTPUT_CSV_FILE_DPCA, index=False, sep=';')
        

@task(name='extract_dpca')
def extract_dpca():
    extractor = CastorToCSV(STUDY_DPCA, CLIENT_ID, CLIENT_SECRET)
    extractor.execute()


@flow(name='castor2csv')
def castor2csv():
    extract_dpca()


if __name__ == '__main__':
    castor2csv()
