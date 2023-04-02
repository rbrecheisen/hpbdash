import os
import logging

from prefect import flow, task
from barbell2.castor.castor2sqlite import CastorToSqlite


STUDY = 'ESPRESSO_v2.0_DPCA'
CLIENT_ID = open(os.path.join(os.environ['HOME'], 'castorclientid.txt'), 'r').readline().strip()
CLIENT_SECRET = open(os.path.join(os.environ['HOME'], 'castorclientsecret.txt'), 'r').readline().strip()
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@task(name='extract_data')
def extract_data():
    extractor = CastorToSqlite(
        STUDY, 
        CLIENT_ID, 
        CLIENT_SECRET, 
        output_db_file=os.path.join(os.environ['HOME'], 'Desktop/castor.db'),
        add_timestamp=True,
        record_offset=0, 
        max_nr_records=5,
        rate_limiting=False,
        nr_secs_before_recreate_session=120,
    )
    extractor.execute()


@flow(name='castor2sqlite')
def castor2sqlite():
    extract_data()


if __name__ == '__main__':
    castor2sqlite()
