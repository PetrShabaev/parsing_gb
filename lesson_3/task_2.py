import json
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh_vacancies"
MONGO_COLLECTION = "vacancies"


def search_data(collection, input_data):
    cursor = collection.find(
        {
            "$or":
                [
                    {"min_salary_border":
                        {
                            "$gt": input_data['salary_border']
                        }},
                    {"max_salary_border":
                        {
                            "$gt": input_data['salary_border']
                        }}
                ],
            "salary_currency": input_data['currency']
        }
    )

    for data in cursor:
        print(data)


def main():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        input_data = {
            "salary_border": int(input('Введите минимальный уровень зарплаты')),
            "currency": input('Введите валюту в формате: "руб.", "USD", "EUR"'),
        }
        search_data(collection, input_data)


if __name__ == "__main__":
    main()
