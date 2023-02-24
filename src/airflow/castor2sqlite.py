import os
import logging
import pendulum

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from barbell2.castor.castor2sqlite import CastorToSqlite

STUDY_NAME = 'ESPRESSO_v2.0_DPCA'
CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dag(schedule='*10 * * * *', start_date=pendulum.now().subtract(minutes=1), catchup=False)
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
            output_db_file=f'/opt/airflow/db/castor_{timestamp}.db',  # This file is written to the Airflow worker container!
            cache=True,
            record_offset=0,
            max_nr_records=1,
            log_level=logging.INFO,
        )
        converter.execute()

    extract_data()

castor2sqlite()


if __name__ == '__main__':
    def main():
        pass
    main()
