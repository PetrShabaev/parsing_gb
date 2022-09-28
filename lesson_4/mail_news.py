import requests
from pymongo import MongoClient
from lxml.html import fromstring

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mail_news"
MONGO_COLLECTION = "news"


HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}


URL = 'https://news.mail.ru/'
PATH_TO_MAIN_NEWS = '//ul[contains(@class, "list_half")]/li[@class="list__item"]'
PATH_TO_NEWS_LINK = './a[@class="list__text"]/@href'
PATH_TO_NEWS_NAME = './a[@class="list__text"]/text()'
PATH_TO_NEWS_PUBLISHED_TIME = './/span[contains(@class,"note__text")]/@datetime'
PATH_TO_SOURCE = '(.//span[@class="breadcrumbs__item"])[last()]/span[@class="note"]/a/span/text()'


def insert_data(news):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:

        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        collection.insert_one(news)


def get_source_and_time(news_link):

    request = requests.get(news_link, headers=HEADERS)
    dom = fromstring(request.text)

    source = dom.xpath(PATH_TO_SOURCE)[0]
    published_time = dom.xpath(PATH_TO_NEWS_PUBLISHED_TIME)[0]

    return source, published_time


def main():
    request = requests.get(URL, HEADERS)

    dom = fromstring(request.text)

    items = dom.xpath(PATH_TO_MAIN_NEWS)

    for item in enumerate(items):
        news_title = item[1].xpath(PATH_TO_NEWS_NAME)[0].strip()
        news_link = item[1].xpath(PATH_TO_NEWS_LINK)[0]

        if "Фото дня" not in news_title:
            source, published_time = get_source_and_time(news_link)

            news = {
                '_id': item[0],
                "source": source,
                "news_title": news_title,
                "news_link": news_link,
                "published_time": published_time
            }

            insert_data(news)


if __name__ == "__main__":
    main()
