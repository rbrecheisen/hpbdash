from airflow import DAG
from airflow.decorators import task


with DAG(
    'castor',
    default_args={},
    description='Pipeline to extract data from Castor EDC',
) as dag:
    @task(task_id='connect')
    def connect(ds=None, **kwargs):
        print('Executing task connect...')
    t1 = connect
    t1
