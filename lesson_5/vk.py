import time
from pymongo import MongoClient
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = "vk"
MONGO_COLLECTION = "posts"


URL = 'https://vk.com/tokyofashion'
PAGE_COUNT = 3

DOMAIN = 'https://vk.com'
SEARCH_POSTS_XPATH = '//div[contains(@id,"page_search")]/div[contains(@id,"post-")]'
POST_LINK_XPATH = './/a[contains(@class,"post_link")]/@href'
POST_DATE_XPATH = './/span[contains(@class,"date")]/text()'
POST_TEXT_XPATH = './/div[contains(@class,"post_text")]/text()'
POST_LIKES_XPATH = './/div[contains(@class,"like_btns")]//span[contains(@class,"count")]/div/text()'
POST_SHARE_XPATH = './/div[contains(@class,"share")]/span[contains(@class,"count")]/text()'
POST_VIEWS_XPATH = './/div[contains(@class,"like_views")]/@title'
POST_MEDIA_XPATH = './/div[contains(@class,"page_post_sized_thumbs")]/a'
POST_VIDEO_XPATH = './/div[contains(@class,"page_post_sized_thumbs")]/a/@href'
POST_PHOTO_XPATH = './/div[contains(@class,"page_post_sized_thumbs")]/a/@style'


def write_data(post):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        collection.insert_one(post)


def get_data():
    with open('index.html', 'r', encoding='utf-8') as file:
        page = file.read()

        dom = fromstring(page)

        posts = dom.xpath(SEARCH_POSTS_XPATH)

        for post in enumerate(posts):
            try:
                post_date = post[1].xpath(POST_DATE_XPATH)[0].replace('\xa0', ' ')
            except:
                post_date = None
            try:
                post_link = DOMAIN + post[1].xpath(POST_LINK_XPATH)[0]
            except:
                post_link = None
            try:
                post_text = ",".join(post[1].xpath(POST_TEXT_XPATH))
            except:
                post_text = None
            try:
                post_likes = int(post[1].xpath(POST_LIKES_XPATH)[0])
            except:
                post_likes = None
            try:
                post_share = int(post[1].xpath(POST_SHARE_XPATH)[0])
            except:
                post_share = None
            try:
                post_views = int(post[1].xpath(POST_VIEWS_XPATH)[0].split(' ')[0])
            except:
                post_views = None
            try:
                if post[1].xpath(POST_VIDEO_XPATH):
                    post_media_link = DOMAIN + post[1].xpath(POST_VIDEO_XPATH)[0]
                else:
                    post_media_link_raw = post[1].xpath(POST_PHOTO_XPATH)
                    post_media_link = []
                    for link in post_media_link_raw:
                        post_media_link.append(link.split('url')[1].replace('(', '').replace(')', ''))
            except:
                post_media_link = None

            post = {
                '_id': post[0] + 1,
                'post_date':  post_date,
                'post_link':  post_link,
                'post_text':  post_text,
                'post_likes': post_likes,
                'post_share':  post_share,
                'post_views': post_views,
                'post_media_link': post_media_link
            }

            write_data(post)


def find_posts(driver, search_word):
    driver.get(URL)
    time.sleep(2)
    search_element = driver.find_element(By.XPATH, '//a[contains(@class,"search")]')
    driver.execute_script(f"window.scrollTo(0, {search_element.location['y'] - 100})")
    time.sleep(1)
    search_element.click()
    time.sleep(1)
    input_field = driver.find_element(By.XPATH, '//div[contains(@class,"ui_search")]/input')
    input_field.send_keys(search_word)
    time.sleep(2)
    input_field.send_keys(Keys.RETURN)


def close_pop_up_window(driver):
    close_element = driver.find_element(By.XPATH,
                                        '//button[contains(@class,"UnauthActionBox__close")]')
    close_element.click()


def get_page_source(search_word):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    try:
        find_posts(driver, search_word)
        for i in range(PAGE_COUNT):
            time.sleep(7)
            try:
                close_pop_up_window(driver)
                time.sleep(5)
            except Exception:
                print('------')
            posts = driver.find_elements(By.XPATH, SEARCH_POSTS_XPATH)
            print(len(posts))
            if not posts:
                break
            actions = ActionChains(driver)
            actions.move_to_element(posts[-1])
            actions.perform()
            time.sleep(5)
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def main():
    search_word = input('Введите слово для поиска')
    get_page_source(search_word)
    get_data()


if __name__ == '__main__':
    main()
