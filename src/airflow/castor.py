from datetime import datetime
from airflow.decorators import dag, task


@dag(schedule=None, start_date=datetime.now())
def castor():
    @task(task_id='connect')
    def connect(ds=None, **kwargs):
        print('Executing task connect...')
    connect()


castor()
