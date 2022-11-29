import os

from barbell2.castor.api import CastorApiClient
from datetime import datetime
from airflow.decorators import dag, task

CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']


@dag(schedule=None, start_date=datetime.now())
def castor():

    @task(task_id='extract_data')
    def extract_data(ds=None, **kwargs):
        client = CastorApiClient(CLIENT_ID, CLIENT_SECRET)
        print(client.studies)

    extract_data()


castor()
