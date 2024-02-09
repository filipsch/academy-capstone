from datetime import datetime, timedelta
from airflow import DAG
from conveyor.operators import ConveyorContainerOperatorV2
role = "capstone_conveyor"

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG, its schedule, and start date
dag = DAG(
    'filip-ingest-weather-dag',
    default_args=default_args,
    description='DAG that ingests open weather data into snowflake',
    schedule_interval="@daily",
    start_date=datetime(2024, 2, 8),
    catchup=False,
)

ConveyorContainerOperatorV2(
    task_id="filip-ingest-weather-task",
    aws_role=role,
    instance_type='mx.micro',
    dag=dag
)
