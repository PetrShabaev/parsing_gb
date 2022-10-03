from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.hh import HhSpider
from jobparser.spiders.sj import SuperJobSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # spider_hh_init_kwargs = {
    #     "query_text": input("Введите запрос")
    # }
    spider_superjob_init_kwargs = {
        "query_text": input("Введите запрос")
    }

    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(HhSpider, **spider_hh_init_kwargs)
    process.crawl(SuperJobSpider, **spider_superjob_init_kwargs)
    process.start()
