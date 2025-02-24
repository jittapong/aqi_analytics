#!/bin/bash
# Add Airflow connection
airflow connections add 'postgres_air_data' \
    --conn-type 'postgres' \
    --conn-host 'postgres_air_data' \
    --conn-login 'admin' \
    --conn-password 'adminpassword' \
    --conn-schema 'air_data' \
    --conn-port '5432'

# Create Airflow admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password adminpassword