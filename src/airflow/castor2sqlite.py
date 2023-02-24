import os
import logging
import pendulum

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from barbell2.castor.castor2sqlite import CastorToSqlite

STUDY_NAME = 'ESPRESSO_v2.0_DPCA'
CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']
OUTPUT_DB_FILE = '/tmp/castor.db'  # DB file is written to data volume accessible via airflow-worker container!

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dag(schedule=None, start_date=pendulum.now().subtract(minutes=1), catchup=False)
def castor2sqlite():

    @task(task_id='extract_data')
    def extract_data():
        timestamp = pendulum.now().strftime('%Y%m%d%H%M%s')
        # context = get_current_context()
        # study_name = context['dag_run'].conf.get('study_name')
        converter = CastorToSqlite(
            study_name=STUDY_NAME,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            output_db_file=f'castor_{timestamp}.db',
            cache=True,
            record_offset=0,
            max_nr_records=1,
            log_level=logging.INFO,
        )
        converter.execute()

    @task(task_id='save_file')
    def save_file():
        timestamp = pendulum.now().strftime('%m-%d-%Y_%H:%M:%S')
        with open('/tmp/{}.txt'.format(timestamp), 'w') as f:
            f.write('hello!')

    extract_data()
    # save_file()

castor2sqlite()


if __name__ == '__main__':
    def main():
        pass
    main()
