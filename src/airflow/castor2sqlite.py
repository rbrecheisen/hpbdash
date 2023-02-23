import os
import logging

from datetime import datetime
from airflow.decorators import dag, task
from barbell2.castor.castor2sqlite import CastorToSqlite

CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']


@dag(schedule=None, start_date=datetime.now())
def castor2sqlite():

    @task(task_id='extract_data')
    def extract_data(ds=None, **kwargs):
        converter = CastorToSqlite(
            study_name='ESPRESSO_v2.0_DPCA',
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            output_db_file='/tmp/castor.db',
            cache=True,
            record_offset=0,
            max_nr_records=1,
            log_level=logging.INFO,
        )
        converter.execute()

    extract_data()

castor2sqlite()
