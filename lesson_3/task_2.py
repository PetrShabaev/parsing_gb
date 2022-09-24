import json
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh_vacancies"
MONGO_COLLECTION = "vacancies"


def search_data(collection):

    cursor = collection.find(
        {
            "min_salary_border":
                {
                    "$gt": 200000
                }
        }
    )

    for data in cursor:
        print(data)


def main():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        search_data(collection)


if __name__ == "__main__":
    main()
