import logging
from airflow import DAG
from airflow.decorators import task
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
from hooks.station import fetch_data
from station.etl import validate_data, parse_data, clean_data, push_to_db

# ✅ Define default arguments for the DAG
default_args = {
    "owner": "bomb",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 24, 10, 28),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,  # Avoid running past DAG runs
}

# ✅ Define the DAG using the TaskFlow API
with DAG(
    "station_data",
    default_args=default_args,
    description="A simple data pipeline for station data",
    schedule_interval="0 * * * *",  # Run hourly
    tags=["station", "ETL"]
) as dag:

    # ✅ Task 1: Fetch Data
    @task
    def fetch_station_data():
        data = fetch_data()
        validate_data(data)
        logging.info(f"Fetched data -> Status: {data['status']}, #Data: {len(data['data'])}")
        return data

    # ✅ Task 2: Parse Data
    @task
    def parse_station_data(fetched_data):
        parsed_data = parse_data(fetched_data)
        logging.info(f"Parsed data -> Example First 3 Rows: {parsed_data[:3]}")
        return parsed_data

    # ✅ Task 3: Clean Data
    @task
    def clean_station_data(parsed_data):
        cleaned_data = clean_data(parsed_data)
        logging.info(f"Cleaned data -> Example First 3 Rows: {cleaned_data[:3]}")
        return cleaned_data

    # ✅ Task 4: Push Data to Database
    @task
    def push_station_data_to_db(cleaned_data):
        conn = PostgresHook(postgres_conn_id="postgres_air_data").get_conn()
        push_to_db(conn, cleaned_data)
        logging.info("Pushed cleaned data to DB successfully.")

    # ✅ Define Task Dependencies
    raw_data = fetch_station_data()
    parsed_data = parse_station_data(raw_data)
    cleaned_data = clean_station_data(parsed_data)
    push_station_data_to_db(cleaned_data)