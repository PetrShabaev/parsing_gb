import scrapy
from scrapy.http import TextResponse
from jobparser.items import JobparserItem

SJ_URL_TEMPLATE = "https://russia.superjob.ru/vacancy/search/?keywords="


class SuperJobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    xpath_routs_for_parse = {
        'url': './/a[contains(@target,"_blank")]/@href'
    }
    xpath_routs_for_parse_item = {
        'title': '//h1/text()',
        'salary': '//h1//following-sibling::span/span[1]/text()',
        'currency': '//h1//following-sibling::span/span[1]/text()'
    }

    def __init__(self, query_text):
        super().__init__()
        start_url = SJ_URL_TEMPLATE + query_text
        self.start_urls = [start_url]

    def parse_item(self, response: TextResponse):
        item = JobparserItem()
        print()
        for field, xpath_rout in self.xpath_routs_for_parse_item.items():
            item[field] = response.xpath(xpath_rout).getall()

        item['source'] = 'superjob'
        item['url'] = response.url
        yield item

    def parse(self, response):
        items = response.xpath('//div[contains(@class,"f-test-vacancy-item")]')

        for item in items:
            url = item.xpath(self.xpath_routs_for_parse['url']).get()
            # url = 'https://russia.superjob.ru/vakansii/inzhener-42940168.html'
            yield response.follow(
                url,
                callback=self.parse_item
            )

        next_page_link = 'https://russia.superjob.ru/' +\
                         response.xpath('//a[contains(@rel,"next") '
                                        'and contains(@class,"dalshe")]/@href').get()
        if next_page_link:
            yield response.follow(
                next_page_link,
                callback=self.parse
            )
