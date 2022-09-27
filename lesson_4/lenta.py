import requests
from pymongo import MongoClient

from lxml.html import fromstring

HEADERS = {
    "accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}

SOURCE = "lenta.ru"
URL = "https://lenta.ru/"
PATH_TO_MAIN_NEWS_DIV = "//div[@class='last24']"
PATH_TO_MAIN_NEWS = "//div[@class='last24']/a"
PATH_TO_NEWS_LINK = "./@href"
PATH_TO_NEWS_NAME = ".//span/text()"
PATH_TO_NEWS_PUBLISHED_TIME = ".//time[@class= 'topic-header__item topic-header__time']/text()"

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "lenta_news"
MONGO_COLLECTION = "news"


def insert_data(news):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        collection.insert_one(news)


def get_published_time(news_link):
    response = requests.get(news_link, headers=HEADERS)
    dom = fromstring(response.text)

    date = dom.xpath(PATH_TO_NEWS_PUBLISHED_TIME)
    return date


def main():
    response = requests.get(URL, headers=HEADERS)
    dom = fromstring(response.text)

    items = dom.xpath(PATH_TO_MAIN_NEWS)

    for item in enumerate(items):
        news = {
            "_id": item[0],
            "source": SOURCE,
            "news_name": item[1].xpath(PATH_TO_NEWS_NAME)[0],
            "news_link": URL + item[1].xpath(PATH_TO_NEWS_LINK)[0],
        }
        news["news_published_time"] = get_published_time(news["news_link"])[0]
        insert_data(news)


if __name__ == "__main__":
    main()
