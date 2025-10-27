from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Basic default arguments for the DAG
default_args = {
    'owner': 'dawid',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 27),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

# Define the DAG
dag = DAG(
    'mongodb_log_pipeline',
    default_args=default_args,
    description='Log Analytics Pipeline',
    schedule_interval='@hourly',
    catchup=False,
    tags=['mongodb', 'logs', 'analytics'],
)

# Generate logs
task_generate = BashOperator(
    task_id='generate_logs',
    bash_command='python /opt/airflow/scripts/generate_logs.py',
    dag=dag,
)

# Run ETL
task_etl = BashOperator(
    task_id='run_etl',
    bash_command='python /opt/airflow/scripts/etl.py',
    dag=dag,
)

# Run analysis
task_analysis = BashOperator(
    task_id='run_analysis',
    bash_command='python /opt/airflow/scripts/analysis.py',
    dag=dag,
)

# Define task dependencies
task_generate >> task_etl >> task_analysis