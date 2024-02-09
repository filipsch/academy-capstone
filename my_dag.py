from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.batch import BatchOperator

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
    'Filip_ingest_weather_data',
    default_args=default_args,
    description='DAG that ingests open weather data into snowflake',
    schedule_interval="@daily",
    start_date=datetime(2024, 2, 8),
    catchup=False,
)

# Define the AWS Batch job operator
run_batch_job = BatchOperator(
    task_id='spark_job',
    job_name='Filip-capstone-job',
    job_queue='academy-capstone-winter-2024-job-queue',  # Specify your AWS Batch job queue here
    job_definition='Filip-capstone-job-definition:3',
    # region_name='eu-west-1', 
    dag=dag,
)

