from datetime import datetime
from barbell2.castor.api import CastorApiClient
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import dag


def print_start():
    print('creating table...')


def print_end():
    print('finished')


@dag(schedule=None, start_date=datetime.now())
def postgresql():

    start = PythonOperator(
        task_id='start',
        python_callable=print_start,
    )

    create_table = PostgresOperator(
        task_id='create_table',
        sql="""
        SET CONNECTION TO castor;
        CREATE TABLE IF NOT EXISTS castor (
            record_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            birth_date DATE NOT NULL
        );
        """,
        postgres_conn_id='postgres',
    )

    end = PythonOperator(
        task_id='end',
        python_callable=print_end,
    )

    start >> create_table >> end


postgresql()
