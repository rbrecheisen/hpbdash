import psycopg2

from datetime import datetime
from barbell2.castor.api import CastorApiClient
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import dag


def print_start():
    print('starting...')


def create_table_callable():
    print('connecting to database...')
    connection = psycopg2.connect(host='postgres-castor', database='postgres', user='castor', password='castor')
    print(connection.info)
    print('closing...')
    connection.close()


def print_end():
    print('done')


@dag(schedule=None, start_date=datetime.now())
def postgresql():

    start = PythonOperator(
        task_id='start',
        python_callable=print_start,
    )

    # create_table = PythonOperator(
    #     task_id='create_table',
    #     python_callable=create_table_callable,
    # )

    create_table = PostgresOperator(
        task_id='create_table',
        sql="""
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
