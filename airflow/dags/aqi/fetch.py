import json
import requests
import logging

# API Endpoint & Token
API_URL = "https://api.waqi.info/feed/"
API_TOKEN = "fe657f17f661e34a738e676c757d7cee1118598f"


# Function to fetch data
def fetch_data(station_uid):
    logging.info("Fetching aqi data from API...")
    response = requests.get(f"{API_URL}@{station_uid}/", params={"token": API_TOKEN})

    print(response)

    if response.status_code == 200:
        data = response.json()
        print(data)
        logging.info(f"API Response: {json.dumps(data, indent=2)}")
        return data
    else:
        logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None
