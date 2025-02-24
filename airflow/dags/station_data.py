import logging
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
from hooks.station import fetch_data
from station.etl import validate_data, parse_data, clean_data, push_to_db

# Default arguments for the DAG
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

# Define the DAG
dag = DAG(
    "station_data",
    default_args=default_args,
    description="A simple data pipeline for station data",
    schedule_interval="0 * * * *",  # Run hourly
)


# Define the tasks
def fetch_data_task(**kwargs):
    data = fetch_data()
    validate_data(data)
    kwargs["ti"].xcom_push(key="fetched_data", value=data)
    logging.info(
        "fetched data -> \nstatus: %s\n#data: %s", data["status"], len(data["data"])
    )


def parse_data_task(**kwargs):
    ti = kwargs["ti"]
    fetched_data = ti.xcom_pull(key="fetched_data", task_ids="fetch_data")
    parsed_data = parse_data(fetched_data)
    ti.xcom_push(key="parsed_data", value=parsed_data)
    logging.info("parsed data -> \nexample_first_3_rows: %s", parsed_data[:3])


def clean_data_task(**kwargs):
    ti = kwargs["ti"]
    parsed_data = ti.xcom_pull(key="parsed_data", task_ids="parse_data")
    clean_data(parsed_data)
    logging.info("cleaned data: \nexample_first_3_rows: %s", parsed_data[:3])


def push_to_db_task(**kwargs):
    ti = kwargs["ti"]
    parsed_data = ti.xcom_pull(key="parsed_data", task_ids="parse_data")
    conn = PostgresHook(postgres_conn_id="postgres_air_data").get_conn()
    push_to_db(conn, parsed_data)
    logging.info("pushed data to db")


fetch_data_operator = PythonOperator(
    task_id="fetch_data",
    python_callable=fetch_data_task,
    provide_context=True,
    dag=dag,
)

parse_data_operator = PythonOperator(
    task_id="parse_data",
    python_callable=parse_data_task,
    provide_context=True,
    dag=dag,
)

clean_data_operator = PythonOperator(
    task_id="clean_data",
    python_callable=clean_data_task,
    provide_context=True,
    dag=dag,
)

push_to_db_operator = PythonOperator(
    task_id="push_to_db",
    python_callable=push_to_db_task,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_data_operator >> parse_data_operator >> clean_data_operator >> push_to_db_operator
