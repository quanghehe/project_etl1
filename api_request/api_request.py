import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("weather_api.log"),  # Ghi log ra file
        logging.StreamHandler()  # Ghi log ra console
    ]
)

logger = logging.getLogger(__name__)

api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"
    
def fetch_data():
    logger.info("Fetching data from API weather....")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        logger.info("API request successful.")
        logger.info(response.json()) 
    except requests.exceptions.RequestException as e:
        logger.error("An error occurred: %s",e)
        raise

def mock_fetch_data():
    return {
        'request': {
            'type': 'City',
            'query': 'New York, United States of America',
            'language': 'en',
            'unit': 'm'
        },
        'location': {
            'name': 'New York',
            'country': 'United States of America',
            'region': 'New York',
            'lat': '40.714',
            'lon': '-74.006',
            'timezone_id': 'America/New_York',
            'localtime': '2025-07-23 02:33',
            'localtime_epoch': 1753237980,
            'utc_offset': '-4.0'
        },
        'current': {
            'temperature': 22,
            'weather_descriptions': ['Clear'],
            'icon': 'http://corldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png',
            'wind_speed': 8,
            'wind_degree': 142,
            'wind_dir': 'SE',
            'pressure': 1023,
            'precip': 0,
            'humidity': 63,
            'cloudcover': 25,
            'feelslike': 22,
            'uv_index': 0,
            'visibility': 16,
            'is_day': 'no',
            'astro': {
                'sunrise': '05:45 AM',
                'sunset': '08:20 PM',
                'moonrise': '03:57 AM',
                'moonset': '08:01 PM',
                'moon_phase': 'Waning Crescent',
                'moon_illumination': 4
            },
            'air_quality': {
                'co': '527.25',
                'no2': '62.53',
                'o3': '40',
                'so2': '16.28',
                'pm2_5': '39.035',
                'pm10': '45.695',
                'us-epa-index': '2',
                'gb-defra-index': '2'
            }
        }
    }