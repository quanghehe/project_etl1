from airflow import DAG
from datetime import datetime,timedelta
import sys
from airflow.operators.python import PythonOperator

sys.path.append('/opt/airflow/api_request')
from insert_record import main 

default_args = {
    'description': 'A dag to orchestrator data',
    'start_date' : datetime(2025,7,20),
}

dag = DAG(
    dag_id = 'weather_id_orchestator',
    default_args = default_args,
    schedule=timedelta(minutes=10), 
    catchup=False 
)

with dag:
    task1 = PythonOperator(
        task_id = 'exemple_task',
        python_callable=main
    )
    