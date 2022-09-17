import requests
from pprint import pprint
import json
import os

from dotenv import load_dotenv

load_dotenv("../secret_info")

TOKEN = os.getenv("TOKEN")
USERNAME = input('Введите имя пользователя')
URL = f"https://api.github.com/users/{USERNAME}/repos"


def write_info(info):
    with open('json_for_task_1.json', 'w') as file:
        json.dump(info, file, indent=4)


def get_headers(token):
    return {"Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}"}


def get_request(url):
    data = []
    headers = get_headers(TOKEN)
    page = 1
    while True:
        request = requests.get(url, headers=headers, params={"page": page})
        if request.status_code == 200:
            if len(request.json()) > 0:
                for item in request.json():
                    print(item.get('full_name'))
                data.extend(request.json())
            else:
                break
        page += 1
    write_info(data)


if __name__ == '__main__':
    get_request(URL)
