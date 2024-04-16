from datetime import datetime, timedelta
from config_data import config


current_date = datetime.now()
tomorrow_date = current_date + timedelta(1)

url = "https://hotels4.p.rapidapi.com"
params = {"q": None, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

headers_get = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

headers_post = {
    "content-type": "application/json",
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

payload_hotels = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001,
    "destination": {"regionId": None},
    "checkInDate": {
        "day": current_date.day,
        "month": current_date.month,
        "year": current_date.year
    },
    "checkOutDate": {
        "day": tomorrow_date.day,
        "month": tomorrow_date.month,
        "year": tomorrow_date.year
    },
    "rooms": [
        {
            "adults": 1
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {"price": {
        "max": None,
        "min": None
    }}
}

payload_details = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001,
    "propertyId": None
}
