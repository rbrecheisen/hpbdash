from airflow.decorators import dag, task


@dag(schedule=None)
def castor():
    @task(task_id='connect')
    def connect(ds=None, **kwargs):
        print('Executing task connect...')
    connect()


castor()
