from lxml.html import fromstring
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import re

URL = 'https://dzen.ru/'

BUTTON_XPATH = '//div[contains(@class,"news__active")]/button/div'
PATH_TO_MAIN_NEWS = '//div[contains(@class,"news__active")]/ul/li'
PATH_TO_NEWS_TITLE = './a/div/span/text()'
PATH_TO_NEWS_LINK = './a/@href'
PATH_TO_SOURCE = './a/div/@title'
PATH_TO_PUBLISHED_DATE = '//div[contains(@class, "news-story__head")]/a/@data-log-id'

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mail_news"
MONGO_COLLECTION = "news"


def get_page_source():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    try:
        driver.get(url=URL)
        time.sleep(1)
        driver.find_element(By.XPATH, BUTTON_XPATH).click()
        time.sleep(1)
        driver.find_element(By.XPATH, BUTTON_XPATH).click()
        time.sleep(3)
        with open("index.html", 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


def get_published_time(news_link):
    published_time = None
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    try:
        driver.get(url=news_link)
        time.sleep(1)
        page = driver.page_source
        dom = fromstring(page)
        date_attribute = dom.xpath(PATH_TO_PUBLISHED_DATE)[0]
        unix_time = int(re.search('(?![a-z-]).............', date_attribute).group())//1000
        published_time = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    return published_time


def insert_data(news):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client['yandex_news']
        collection = db['news']

        collection.insert_one(news)


def parsing_html():
    with open('index.html', 'r', encoding='utf-8') as file:
        page = file.read()
        dom = fromstring(page)

        items = dom.xpath(PATH_TO_MAIN_NEWS)

        for item in enumerate(items):
            news_id = item[0]
            news_title = item[1].xpath(PATH_TO_NEWS_TITLE)[0].strip().replace('\xa0', ' ')
            news_link = item[1].xpath(PATH_TO_NEWS_LINK)[0]
            source = item[1].xpath(PATH_TO_SOURCE)[0]
            published_time = get_published_time(news_link)

            news = {
                '_id': news_id,
                'news_title': news_title,
                'news_link': news_link,
                'source': source,
                'published_time': published_time
            }
            insert_data(news)


def main():
    get_page_source()
    parsing_html()


if __name__ == '__main__':
    main()
