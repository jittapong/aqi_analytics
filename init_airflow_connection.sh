#!/bin/bash
airflow connections add 'postgres_air_data' \
    --conn-type 'postgres' \
    --conn-host 'postgres_air_data' \
    --conn-login 'admin' \
    --conn-password 'adminpassword' \
    --conn-schema 'air_data' \
    --conn-port '5432'