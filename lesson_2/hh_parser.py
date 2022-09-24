from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_vacancy_name():
    return input('Введите название вакансии или ключевое слово')


def get_request(url):
    html = None
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe", options=options
    )
    try:
        driver.get(url=url)
        time.sleep(3)
        html = driver.page_source
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    return html


def get_dom(request):
    return BeautifulSoup(request, "html.parser")


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
                min_salary_border = int(salary_list_info[0].replace(" ", ''))
                max_salary_border = int(salary_list_info[2].replace(" ", ''))
                salary_currency = salary_list_info[3]
            elif "от" in salary:
                min_salary_border = int(salary_list_info[1].replace(" ", ''))
                max_salary_border = None
                salary_currency = salary_list_info[2]
            elif "до" in salary:
                min_salary_border = None
                max_salary_border = int(salary_list_info[1].replace(" ", ''))
                salary_currency = salary_list_info[2]
        except AttributeError:
            min_salary_border = None
            max_salary_border = None
            salary_currency = None
        try:
            employer = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).get_text().\
                replace(" ", ' ')
        except AttributeError:
            employer = "Не указан"

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
    URL = f"https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&" \
          f"text={PARAMS['text']}&from=suggest_post&page={PARAMS['page']}"
    vacancies_list = []
    while True:
        request = get_request(URL)
        soup = get_dom(request)
        if soup.find('div', attrs={"class": "serp-item"}) is not None:
            vacancies_list.extend(get_data(soup))
            # pprint(vacancies_list)
        else:
            break
        PARAMS["page"] += 1
        URL = f"https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=" \
              f"description&text={PARAMS['text']}&from=suggest_post&page={PARAMS['page']}"
    with open("vacancies.json", "w", encoding="utf-8") as file:
        json.dump(vacancies_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
