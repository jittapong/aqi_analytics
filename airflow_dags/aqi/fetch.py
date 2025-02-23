import json
import requests
import logging

# API Endpoint & Token
API_URL = "https://api.waqi.info/v2/map/bounds/"
API_TOKEN = "fe657f17f661e34a738e676c757d7cee1118598f"

# Bounding box for entire Thailand
LAT_LNG_BOUNDS = ["5.451446,96.135864,21.053264,105.847778"]
# LAT_LNG_BOUNDS = ["16.562493,96.811523,20.581367,101.755371"] # Bounding box for North of Thailand


# Function to fetch data
def fetch_data():
    logging.info("Fetching air quality data from API...")
    response = requests.get(
        API_URL, params={"latlng": LAT_LNG_BOUNDS, "token": API_TOKEN}
    )

    print(response)

    if response.status_code == 200:
        data = response.json()
        print(data)
        logging.info(f"API Response: {json.dumps(data, indent=2)}")
        return data
    else:
        logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None
