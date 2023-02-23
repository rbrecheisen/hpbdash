import os
import logging

from datetime import datetime
from airflow.decorators import dag, task
from barbell2.castor.castor2sqlite import CastorToSqlite

STUDY_NAME = os.environ['CASTOR_STUDY_NAME']
CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dag(schedule=None, start_date=datetime.now())
def castor2sqlite():

    @task(task_id='extract_data')
    def extract_data(study_name, client_id, client_secret):
        if study_name is None:
            study_name = STUDY_NAME
            client_id = CLIENT_ID
            client_secret = CLIENT_SECRET
            LOGGER.info('Using environment STUDY_NAME, CLIENT_ID and CLIENT_SECRET')
        else:
            LOGGER.info('Using context STUDY_NAME, CLIENT_ID and CLIENT_SECRET')
        converter = CastorToSqlite(
            study_name=study_name,
            client_id=client_id,
            client_secret=client_secret,
            output_db_file='/tmp/castor.db',  # Note: DB file is written to data volume accessible via airflow-worker container!
            cache=True,
            record_offset=0,
            max_nr_records=1,
            log_level=logging.INFO,
        )
        converter.execute()

    extract_data()

castor2sqlite()
