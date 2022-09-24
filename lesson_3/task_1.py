
import json
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh_vacancies"
MONGO_COLLECTION = "vacancies"


def main():
    with open("../lesson_2/vacancies.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]

        collection = db[MONGO_COLLECTION]

        collection.insert_many(data)


if __name__ == "__main__":
    main()
