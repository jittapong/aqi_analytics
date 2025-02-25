import logging
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
from station.etl import get_all_stations
from aqi.etl import parse_data, validate_data, clean_data, push_to_db
from hooks.aqi import fetch_data

# ✅ Define default arguments
default_args = {
    "owner": "bomb",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 24, 10, 28),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# ✅ Create DAG
with DAG(
    "aqi_data",
    default_args=default_args,
    description="Fetch and process AQI data for all stations",
    schedule_interval="0 * * * *",  # Run hourly
    max_active_tasks=10,  # ✅ Limit number of concurrent tasks globally
    tags=["AQI", "ETL"]
) as dag:

    # ✅ Task 1: Fetch all station IDs from the database
    @task
    def fetch_all_stations():
        conn = PostgresHook(postgres_conn_id="postgres_air_data").get_conn()
        stations = get_all_stations(conn)  # Returns a list of station UIDs
        logging.info(f"Fetched {len(stations)} stations from the database.")
        return stations  # This is passed to `.expand()`

    # ✅ Task 2: Fetch and Process AQI Data for Each Station
    @task
    def fetch_and_process_aqi_data(station_uid):
        """Fetch and process AQI data for a given station."""
        logging.info(f"Fetching AQI data for station {station_uid}...")
        data = fetch_data(station_uid)

        if validate_data(data):
            parsed_data = parse_data(data)
            cleaned_data = clean_data(parsed_data)
            
            conn = PostgresHook(postgres_conn_id="postgres_air_data").get_conn()
            push_to_db(conn, cleaned_data)
            logging.info(f"Data for station {station_uid} processed and pushed to the database.")
        else:
            logging.warning(f"Skipping station {station_uid} due to invalid data.")

    # ✅ Set task dependencies correctly
    stations = fetch_all_stations()
    fetch_and_process_aqi_data.expand(station_uid=stations)