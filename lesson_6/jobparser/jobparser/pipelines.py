# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

MONGO_LOCALHOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'scrapy_vacancies'


class JobparserPipeline:
    def convert_string_list_to_string(self, string_list):
        return ' '.join(string_list)

    def get_salary_currency(self, salary_list):
        if 'з/п не указана' in salary_list or 'По договорённости' in salary_list:
            return None
        return salary_list[-1]

    def parse_salary(self, item):
        print()
        if 'з/п не указана' in item['salary']:
            item['salary_min'] = None
            item['salary_max'] = None
        elif 'от ' == item['salary'][0] and ' до ' == item['salary'][2]:
            item['salary_min'] = int(item['salary'][1].replace('\xa0', ''))
            item['salary_max'] = int(item['salary'][3].replace('\xa0', ''))
        elif 'до ' == item['salary'][0]:
            item['salary_min'] = None
            item['salary_max'] = int(item['salary'][1].replace('\xa0', ''))
        else:
            item['salary_min'] = int(item['salary'][1].replace('\xa0', ''))
            item['salary_max'] = None

    def parse_salary_sj(self, item):
        print()
        if 'По договорённости' in item['salary']:
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = self.get_salary_currency(item['currency'])
        elif 'от' == item['salary'][0]:
            item['salary_min'] = ''.join(item['salary'][-1].replace('\xa0', ' ').split(' ')[:2])
            item['salary_max'] = None
            item['currency'] = item['currency'][-1].replace('\xa0', ' ').split(' ')[-1]
        elif 'до' == item['salary'][0]:
            item['salary_max'] = ''.join(item['salary'][-1].replace('\xa0', ' ').split(' ')[:2])
            item['salary_min'] = None
            item['currency'] = item['currency'][-1].replace('\xa0', ' ').split(' ')[-1]
        else:
            if len(item['salary']) > 3:
                item['salary_min'] = item['salary'][0].replace('\xa0', '').replace('\xa0', '')
                item['salary_max'] = item['salary'][1].replace('\xa0', '').replace('\xa0', '')
                item['currency'] = self.get_salary_currency(item['currency'])
            else:
                item['salary_min'] = item['salary'][0].replace('\xa0', '').replace('\xa0', '')
                item['salary_max'] = item['salary'][0].replace('\xa0', '').replace('\xa0', '')
                item['currency'] = self.get_salary_currency(item['currency'])

    def write_data(self, item, spider):
        with MongoClient(MONGO_LOCALHOST, MONGO_PORT) as client:
            db = client[MONGO_DB]
            collection = db[spider.name]

            collection.insert_one(item)

    def process_item(self, item, spider):
        item['title'] = self.convert_string_list_to_string(item['title'])
        if spider.name == 'hh':
            self.parse_salary(item)
            item['currency'] = self.get_salary_currency(item['currency'])
        else:
            self.parse_salary_sj(item)
        del item['salary']
        self.write_data(item, spider)

        return item
