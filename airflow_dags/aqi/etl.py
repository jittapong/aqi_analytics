import logging
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

    stations = []
    for station in data["data"]:
        stations.append(
            {
                "uid": station.get("uid"),
                "aqi": station.get("aqi"),
                "latitude": station.get("lat"),
                "longitude": station.get("lon"),
                "station_name": station["station"].get("name"),
                "timestamp": station["station"].get("time"),
            }
        )

    logging.info(f"Extracted {len(stations)} stations.")
    df = pd.DataFrame(stations)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


def clean_data(data):
    # Drop rows where 'uid' is non-integer
    data = data[pd.to_numeric(data["uid"], errors="coerce").notnull()]
    data["uid"] = data["uid"].astype(int)

    # Validate latitude and longitude
    data = data[
        (data["latitude"].between(-90, 90)) & (data["longitude"].between(-180, 180))
    ]

    # If 'aqi' is non-integer, fill with None
    data["aqi"] = pd.to_numeric(data["aqi"], errors="coerce")
    data["aqi"] = data["aqi"].apply(
        lambda x: None if pd.isna(x) else int(x) if x.is_integer() else None
    )

    # If 'stationname' is invalid string, replace with empty string
    data["station_name"] = data["station_name"].apply(
        lambda x: x if isinstance(x, str) else ""
    )

    return data


# Function to insert data into PostgreSQL
def push_to_db(conn, stations):
    cursor = conn.cursor()

    # SQL command to create the station_info table if it does not exist
    create_station_info_table_query = """
    CREATE TABLE IF NOT EXISTS station_info (
        id SERIAL PRIMARY KEY,
        uid INTEGER UNIQUE,
        latitude FLOAT,
        longitude FLOAT,
        station_name VARCHAR(255)
    );
    """

    # SQL command to create the aqi_data table if it does not exist
    create_aqi_data_table_query = """
    CREATE TABLE IF NOT EXISTS aqi_data (
        id SERIAL PRIMARY KEY,
        uid INTEGER,
        aqi INTEGER,
        timestamp TIMESTAMP,
        UNIQUE(uid, timestamp),
        FOREIGN KEY (uid) REFERENCES station_info(uid)
    );
    """

    # Execute the SQL commands
    cursor.execute(create_station_info_table_query)
    cursor.execute(create_aqi_data_table_query)
    conn.commit()

    insert_station_info_query = """
    INSERT INTO station_info (uid, latitude, longitude, station_name)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (uid) DO NOTHING
    """

    insert_aqi_data_query = """
    INSERT INTO aqi_data (uid, aqi, timestamp)
    VALUES (%s, %s, %s)
    ON CONFLICT (uid, timestamp) DO NOTHING
    """

    for station in stations.itertuples(index=False):
        cursor.execute(
            insert_station_info_query,
            (
                station.uid,
                station.latitude,
                station.longitude,
                station.station_name,
            ),
        )
        cursor.execute(
            insert_aqi_data_query,
            (
                station.uid,
                (
                    station.aqi
                    if not pd.isna(station.aqi) and station.aqi != "-"
                    else None
                ),
                station.timestamp,
            ),
        )

    conn.commit()
    cursor.close()
    logging.info(f"Inserted {len(stations)} records into the database.")
