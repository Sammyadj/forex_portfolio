import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
OANDA_API_URL = os.getenv("OANDA_API_URL")
OANDA_STREAM_URL = os.getenv("OANDA_STREAM_URL")
SECURE_HEADER={'Authorization': f'Bearer {API_KEY}', }


def get_account_instruments(instrument=None):
    url = f"{OANDA_API_URL}/accounts/{ACCOUNT_ID}/instruments"
    params = {}
    if instrument:
        params['instruments'] = instrument
    response = requests.get(url, headers=SECURE_HEADER, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


def get_current_price(instrument_name):
    url = f"{OANDA_API_URL}/accounts/{ACCOUNT_ID}/pricing"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    params = {'instruments': instrument_name}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = data.get('prices', [])
        if prices:
            bid_price = float(prices[0]['bids'][0]['price'])
            ask_price = float(prices[0]['asks'][0]['price'])
            return bid_price, ask_price
    else:
        print(f"Failed to fetch prices: {response.text}")
    return None, None


def fetch_candle_data(instrument_name, count=100, granularity='H1'):
    url = f"{OANDA_API_URL}/accounts/{ACCOUNT_ID}/instruments/{instrument_name}/candles"
    params = {
        'count': count,
        'granularity': granularity,
        'price': 'M'
    }
    response = requests.get(url, headers=SECURE_HEADER, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}
