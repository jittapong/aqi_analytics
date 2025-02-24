FROM --platform=linux/amd64 apache/airflow:2.10.4

RUN pip install ccxt==4.1.100 \
  airflow-provider-great-expectations==0.2.7 \
  papermill==2.6.0 \
  apache-airflow-providers-papermill==3.9.0 \
  pytest