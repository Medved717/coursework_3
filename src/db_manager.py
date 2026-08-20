import psycopg2
from dotenv import load_dotenv
import os

from src.api_client import APICLIENT


class DBMANAGER:

    def __init__(self, list_vacanccies=None):
        if list_vacanccies == None:
            list_vacanccies = APICLIENT.get_response_data('hh_vacancies.json')
        else:
            self.list_vacanccies=list_vacanccies


    def get_companies_and_vacancies_count(self):
        '''Получает список всех компаний и количество вакансий у каждой компании.'''

        # Устанавливаем связь с файлом .env для получения скрытых данных.
        load_dotenv()
        db_password = os.getenv('db_password')

        # Устанавливаем соединение с использованием параметров, после чего устанавливаем курсор.
        conn = psycopg2.connect(host='localhost', port='5432', user='postgres', password=db_password, dbname='coursework_3')
        cur = conn.cursor()

        # Демонстрируем сведения по вакансиям в каждой компании.
        cur.execute('''SELECT company_name, count_vacancy FROM company''')
        result = cur.fetchall()

        conn.commit()      # Комитим изменения в базе данных.
        cur.close()        # Закрываем курсор.
        conn.close()       # Закрываем соединение.

        # Оставил возвращение на всякий случай для возможного использования.
        return result

    def get_all_vacancies(self):
        '''Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.'''

        list_result = []

        for vacancy in self.list_vacanccies:
            company_name = vacancy.get('employer', {}).get('name', {})
            vacancy_name = vacancy.get('name', {})
            salary_from = vacancy.get('salary', {}).get('from', {})
            salary_to = vacancy.get('salary', {}).get('to', {})
            url_vacancy = vacancy.get('alternate_url', {})

            dict_items = {}
            dict_items['company_name'] = company_name
            dict_items['vacancy_name'] = vacancy_name
            dict_items['salary_from'] = salary_from
            dict_items['salary_to'] = salary_to
            dict_items['url_vacancy'] = url_vacancy

            list_result.append(dict_items)

        load_dotenv()
        password = os.getenv('db_password')

        conn = psycopg2.connect(user='postgres', password=password, port='5432',
                                dbname='coursework_3', host='localhost')
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS start_vacancy (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            vacancy_name VARCHAR(100) NOT NULL,
            salary_from VARCHAR(100) NOT NULL,
            salary_to VARCHAR(100) NOT NULL,
            url_vacancy VARCHAR(350) NOT NULL
        )''')


        for vacancy in list_result:
            cur.execute('''INSERT INTO start_vacancy (company_name, vacancy_name, salary_from, salary_to, url_vacancy) VALUES (%s, %s, %s, %s, %s)''',
                        (vacancy['company_name'],
                        vacancy['vacancy_name'],
                        vacancy['salary_from'],
                        vacancy['salary_to'],
                        vacancy['url_vacancy']))
        conn.commit()
        cur.close()
        conn.close()
        return list_result










# obj_1 = DBMANAGER(APICLIENT.get_response_data('hh_vacancies.json'))
# result = obj_1.get_companies_and_vacancies_count()
# print(result)


obj_1 = DBMANAGER(APICLIENT.get_response_data('hh_vacancies.json'))
result = obj_1.get_all_vacancies()
for i in result:
    print(i)