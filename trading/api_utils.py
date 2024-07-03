import requests

API_KEY = "867f258a6a978d867493454cba2b27ff-97f17371b95cbe3171cf608c46a51c91"
ACCOUNT_ID = "101-004-29382789-001"
OANDA_URL = 'https://api-fxpractice.oanda.com/v3'

SECURE_HEADER = {
    'Authorization': f'Bearer {API_KEY}',
}


def get_account_instruments():
    url = f"{OANDA_URL}/accounts/{ACCOUNT_ID}/instruments"
    response = requests.get(url, headers=SECURE_HEADER)
    return response.json()


def fetch_candle_data(instrument_name, count=100, granularity='H1'):
    url = f"{OANDA_URL}/accounts/{ACCOUNT_ID}/instruments/{instrument_name}/candles"
    params = {
        'count': count,
        'granularity': granularity,
        'price': 'M'
    }
    response = requests.get(url, headers=SECURE_HEADER, params=params)
    return response.json()
