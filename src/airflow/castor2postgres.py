import os
import psycopg2

from barbell2.castor.api import CastorApiClient
from datetime import datetime
from airflow.decorators import dag, task

CLIENT_ID = os.environ['CASTOR_CLIENT_ID']
CLIENT_SECRET = os.environ['CASTOR_CLIENT_SECRET']


def init_table(db_session):
    db_cursor = db_session.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS castor (
        record_id SERIAL PRIMARY KEY,
        patient_id VARCHAR NOT NULL,
        gender VARCHAR NOT NULL,
        birth_date DATE NOT NULL,
        weight INT,
        bmi REAL,
        surgery_date DATE NOT NULL,
        hospital_stay INT,
        complications INT
    );
    """
    db_cursor.execute(sql)
    db_session.commit()


def get_client_data(client):
    data = {}
    print('getting study ID from client...')
    study_id = client.get_study_id(client.get_study('ESPRESSO_v2.0_DPCA'))
    print('getting fields...')
    fields = client.get_fields(study_id)
    for k in data.keys():
        print(client.get_field(fields, k))
    return data


@dag(schedule=None, start_date=datetime.now())
def castor2postgres():

    @task(task_id='extract_data')
    def extract_data(ds=None, **kwargs):
        print('connecting to Castor...')
        client = CastorApiClient(CLIENT_ID, CLIENT_SECRET)
        print('getting data...')
        client_data = get_client_data(client)
        print(client_data)
        # print('connecting to Postgres database...')
        # db_session = psycopg2.connect(host='postgres-castor', database='postgres', user='castor', password='castor')

    extract_data()


castor2postgres()
