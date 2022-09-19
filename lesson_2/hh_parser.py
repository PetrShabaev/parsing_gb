from pprint import pprint
import lxml
import requests
from bs4 import BeautifulSoup
import json
import time


def get_vacancy_name():
    return input('Введите название вакансии или ключевое слово')


def get_request(url, params, headers):
    request = requests.get(url, params=params, headers=headers)
    if request.status_code == 200:
        return request
    return None


def get_dom(request):
    return BeautifulSoup(request.content, "html.parser")


def get_data(soup):
    vacancies_per_page = []

    # vacancies = soup.find_all('div', attrs={"class": "vacancy-serp-item-body"})
    vacancies = soup.find('div', {'data-qa': 'vacancy-serp__results'}) \
        .find_all('div', {'class': 'serp-item'})
    print(len(vacancies))
    for vacancy in vacancies:
        vacancy_name = vacancy.find("a", "serp-item__title").get_text()
        vacancy_link = vacancy.find("a", "serp-item__title").get('href')
        try:
            salary = vacancy.find("span", "bloko-header-section-3").get_text()
            salary_list_info = salary.split(' ')
            if " – " in salary:
                min_salary_border = salary_list_info[0]
                max_salary_border = salary_list_info[2]
                salary_currency = salary_list_info[3]
            elif "от" in salary:
                min_salary_border = salary_list_info[1]
                max_salary_border = "Не указана"
                salary_currency = salary_list_info[2]
            elif "до" in salary:
                min_salary_border = "Не указана"
                max_salary_border = salary_list_info[1]
                salary_currency = salary_list_info[2]
        except AttributeError as e:
            min_salary_border = "Не указана"
            max_salary_border = "Не указана"
            salary_currency = "Не указано"
        employer = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).get_text()

        vacancies_per_page.append({
            'vacancy_name': vacancy_name,
            'vacancy_link': vacancy_link,
            'min_salary_border': min_salary_border,
            'max_salary_border': max_salary_border,
            'salary_currency':  salary_currency,
            'employer': employer,
        })

    return vacancies_per_page


def main():
    PARAMS = {
        "text": get_vacancy_name(),
        "page": 0,
    }
    URL = "https://spb.hh.ru/search/vacancy"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36"
    }
    vacancies_list = []
    while True:
        request = get_request(URL, PARAMS, HEADERS)
        soup = get_dom(request)
        if soup.find('div', attrs={"class": "serp-item"}) is not None:
            vacancies_list.extend(get_data(soup))
            PARAMS["page"] += 1
            # pprint(vacancies_list)
            time.sleep(1)
        else:
            break


if __name__ == "__main__":
    main()
