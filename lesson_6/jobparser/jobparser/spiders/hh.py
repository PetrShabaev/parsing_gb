# from typing import Optional

import scrapy
from scrapy.http import TextResponse
from jobparser.items import JobparserItem

HH_URL_TEMPLATE = 'https://spb.hh.ru/search/vacancy?search_field=name&' \
                  'search_field=company_name&search_field=description&text='


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['spb.hh.ru']
    xpath_routs_for_parse = {
        'title': '//a[contains(@class,"_title")/text()]',
        'url': './/a[contains(@class,"_title")]/@href'
    }
    xpath_routs_for_parse_item = {
        'title': '//h1[contains(@data-qa,"-title")]//text()',
        'salary': '//span[contains(@data-qa,"salary")]/text()',
        'currency': '//span[contains(@data-qa,"-salary")]/text()'
    }

    def __init__(self, query_text, _id):
        super().__init__()
        start_url = HH_URL_TEMPLATE + query_text
        self.start_urls = [start_url]
        self._id = _id

    def parse_item(self, response: TextResponse, **kwargs):
        item = JobparserItem()
        item['_id'] = kwargs['_id']
        for field, xpath_rout in self.xpath_routs_for_parse_item.items():
            item[field] = response.xpath(xpath_rout).getall()
        item['source'] = 'hh'
        item['url'] = response.url
        yield item

    def parse(self, response: TextResponse, **kwargs):
        items = response.xpath('//div[@class="serp-item"]')
        for item in items:
            self._id += 1
            url = item.xpath(self.xpath_routs_for_parse['url']).get()
            yield response.follow(
                url,
                callback=self.parse_item,
                cb_kwargs={'_id': self._id}
            )
        next_page_link = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse, cb_kwargs={'_id': self._id})

