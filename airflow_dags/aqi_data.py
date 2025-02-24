from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from station.etl import get_all_stations
from aqi.etl import fetch_data, parse_data, clean_data, push_to_db

# Define default arguments
default_args = {
    "owner": "bomb",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 23, 10, 28),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,  # Avoid running past DAG runs
}

# Create the DAG
dag = DAG(
    "aqi_data",
    default_args=default_args,
    description="A simple DAG to fetch and process AQI data",
    schedule_interval="0 * * * *",  # Run hourly
)


# Define tasks
def fetch_all_stations(**kwargs):
    return get_all_stations()


fetch_stations_task = PythonOperator(
    task_id="fetch_all_stations",
    python_callable=fetch_all_stations,
    provide_context=True,
    dag=dag,
)


def fetch_aqi_data(station_uid, **kwargs):
    return fetch_data(station_uid)


fetch_data_tasks = []
for station_uid in get_all_stations():
    task = PythonOperator(
        task_id=f"fetch_data_{station_uid}",
        python_callable=fetch_aqi_data,
        op_args=[station_uid],
        provide_context=True,
        dag=dag,
    )
    fetch_data_tasks.append(task)


def process_data(**kwargs):
    parse_data()
    clean_data()
    push_to_db()


process_data_task = PythonOperator(
    task_id="process_data",
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_stations_task >> fetch_data_tasks >> process_data_task
