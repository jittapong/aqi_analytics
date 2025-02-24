import logging
import json
import pandas as pd


# Function to validate data
def validate_data(data):
    if not data or "status" not in data or data["status"] != "ok" or "data" not in data:
        raise ValueError("Invalid API Response: Missing required fields.")

    logging.info("Data validation successful!")


# Function to parse data
def parse_data(data):
    if not data or "data" not in data:
        logging.warning("No stations data found!")
        return pd.DataFrame()

    aqi = {}
    aqi["idx"] = data["data"].get("idx")
    aqi["address"] = data["data"]["city"].get("name")
    aqi["aqi"] = data["data"]["iaqi"].get("pm25", {}).get("v")
    aqi["dew"] = data["data"]["iaqi"].get("dew", {}).get("v")
    aqi["h"] = data["data"]["iaqi"].get("h", {}).get("v")
    aqi["o3"] = data["data"]["iaqi"].get("o3", {}).get("v")
    aqi["p"] = data["data"]["iaqi"].get("p", {}).get("v")
    aqi["pm10"] = data["data"]["iaqi"].get("pm10", {}).get("v")
    aqi["pm25"] = data["data"]["iaqi"].get("pm25", {}).get("v")
    aqi["r"] = data["data"]["iaqi"].get("r", {}).get("v")
    aqi["t"] = data["data"]["iaqi"].get("t", {}).get("v")
    aqi["w"] = data["data"]["iaqi"].get("w", {}).get("v")
    aqi["timestamp"] = data["data"]["time"].get("iso")
    aqi["forecast"] = json.dumps(data["data"]["forecast"].get("daily"))

    df = pd.DataFrame(aqi, index=[0])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df


def clean_data(data):
    # TODO
    return data


# Function to insert data into PostgreSQL
def push_to_db(conn, data):
    cursor = conn.cursor()

    # SQL command to create the aqi_data table if it does not exist
    create_aqi_data_table_query = """
    CREATE TABLE IF NOT EXISTS aqi_data (
        id SERIAL PRIMARY KEY,
        idx INTEGER,
        address VARCHAR(255),
        aqi FLOAT,
        dew FLOAT,
        h FLOAT,
        o3 FLOAT,
        p FLOAT,
        pm10 FLOAT,
        pm25 FLOAT,
        r FLOAT,
        t FLOAT,
        w FLOAT,
        timestamp TIMESTAMP,
        forecast JSONB
    );
    """

    # Execute the SQL command
    cursor.execute(create_aqi_data_table_query)
    conn.commit()

    insert_aqi_data_query = """
    INSERT INTO aqi_data (idx, address, aqi, dew, h, o3, p, pm10, pm25, r, t, w, timestamp, forecast)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for row in data.itertuples(index=False):
        cursor.execute(
            insert_aqi_data_query,
            (
                row.idx,
                row.address,
                row.aqi,
                row.dew,
                row.h,
                row.o3,
                row.p,
                row.pm10,
                row.pm25,
                row.r,
                row.t,
                row.w,
                row.timestamp,
                row.forecast,
            ),
        )

    conn.commit()
    cursor.close()
    logging.info(f"Inserted aqi data into the database.")
