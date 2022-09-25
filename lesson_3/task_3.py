import json
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh_vacancies"
MONGO_COLLECTION = "vacancies"


def write_new_vacancy(collection, vacancy):
    collection.update_one(
        {
            "vacancy_link": vacancy["vacancy_link"]
        },
        {
          "$set": vacancy
        },
        upsert=True
    )


def main():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        with open("../lesson_2/vacancies.json", 'r', encoding="utf-8") as file:
            data = json.load(file)

            for vacancy in data:
                if vacancy['vacancy_link'] == "https://spb.hh.ru/vacancy/694114437777?" \
                                              "from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=python":
                    write_new_vacancy(collection, vacancy)


if __name__ == "__main__":
    main()
