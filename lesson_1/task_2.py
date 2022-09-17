import os
from dotenv import load_dotenv
import requests

load_dotenv("../secret_info")

API_key = os.getenv("API_key")
city_name = input('Введите название города')
URL = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}'


def get_request(url):
    request = requests.get(url, params={"units": "metric"})
    if request.status_code == 200:
        print(request.json())


if __name__ == "__main__":
    get_request(URL)
