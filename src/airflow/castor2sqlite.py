import os
import logging

from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from barbell2.castor.castor2sqlite import CastorToSqlite

CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dag(schedule_interval='@hourly', start_date=datetime.now())
def castor2sqlite():

    @task(task_id='extract_data')
    def extract_data():
        context = get_current_context()
        # study_name = context['dag_run'].conf.get('study_name')
        study_name = 'ESPRESSO_v2.0_DPCA'
        converter = CastorToSqlite(
            study_name=study_name,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            output_db_file='/tmp/castor.db',  # Note: DB file is written to data volume accessible via airflow-worker container!
            cache=True,
            record_offset=0,
            max_nr_records=1,
            log_level=logging.INFO,
        )
        converter.execute()

    @task(task_id='save_file')
    def save_file():
        """ This is what should happen:
            (1) Generate timestamp now()
            (2) Write file called timestamp.txt
        """
        timestamp = datetime.now().strftime('%m-%d-%Y_%H:%M:%S')
        with open('/tmp/{}.txt'.format(timestamp), 'w') as f:
            f.write('hello!')

    # extract_data()
    save_file()

castor2sqlite()
