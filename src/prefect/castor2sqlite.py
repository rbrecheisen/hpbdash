import os
import logging

from datetime import datetime
from prefect import flow, task
from barbell2.castor.castor2sqlite import CastorToSqlite

STUDY_NAME = 'ESPRESSO_v2.0_DPCA'
CLIENT_ID = open(os.path.join(os.environ['HOME'], 'castorclientid.txt'), 'r').readline().strip()
CLIENT_SECRET = open(os.path.join(os.environ['HOME'], 'castorclientsecret.txt'), 'r').readline().strip()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@task(name='extract_data')
def extract_data():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    converter = CastorToSqlite(
        study_name=STUDY_NAME,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        output_db_file=f'/tmp/castor_{timestamp}.db',
        cache=True,
        record_offset=0,
        max_nr_records=1,
        log_level=logging.INFO,
    )
    converter.execute()

@flow(name='castor2sqlite')
def castor2sqlite():
    extract_data()

castor2sqlite()
