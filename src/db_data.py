from os import getenv

import psycopg2
from dotenv import load_dotenv
import os

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.api_client import ApiClient

class DbSave:
    """Класс для создания базы данных и сохранения таблиц компаний и вакансий."""

    def __init__(self, list_vacanccies=None):
        if list_vacanccies == None:
            list_vacanccies = ApiClient.get_response_data('hh_vacancies.json')
        else:
            self.list_vacanccies=list_vacanccies

    @staticmethod
    def create_data_base(name_data_base):
        """Создание базы данных для работы с вакансиями."""

        try:
            load_dotenv()
            password = os.getenv('db_password')
            conn = psycopg2.connect(
                user='postgres',
                password=password,
                host='localhost',
                port='5432',
                dbname='postgres'
            )
            cur = conn.cursor()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur.execute(f'''CREATE DATABASE {name_data_base}''')
            print(f'База данных: {name_data_base} успешно создана.')
        except Exception as e:
            print(f'Произошла ошибка! {e}')
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def create_table_company(self, db_name):
        """Метод создает таблицу вакансий в базе данных с указанием названия id вакансии,
        названия вакансии, названия компании, зарплаты и ссылки на вакансию."""

        list_result = []

        for vacancy in self.list_vacanccies:
            vacancy_name = vacancy.get('name', {})
            company_name = vacancy.get('employer', {}).get('name', {})
            salary_from = vacancy.get('salary', {}).get('from', {})
            salary_to = vacancy.get('salary', {}).get('to', {})
            url_vacancy = vacancy.get('alternate_url', {})

            dict_items = {}
            dict_items['vacancy_name'] = vacancy_name
            dict_items['company_name'] = company_name
            dict_items['salary_from'] = salary_from
            dict_items['salary_to'] = salary_to
            dict_items['url_vacancy'] = url_vacancy

            list_result.append(dict_items)

        load_dotenv()
        password = os.getenv('db_password')

        conn = psycopg2.connect(user='postgres', password=password, port='5432',
                                dbname=db_name, host='localhost')
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS list_vacancy (
            vacancy_id SERIAL PRIMARY KEY,
            vacancy_name VARCHAR(100) NOT NULL,
            company_name VARCHAR(100) NOT NULL,
            salary_from VARCHAR(100) NOT NULL,
            salary_to VARCHAR(100) NOT NULL,
            url_vacancy VARCHAR(350) NOT NULL
        )''')


        for vacancy in list_result:
            cur.execute('''INSERT INTO list_vacancy (vacancy_name, company_name, salary_from, salary_to, url_vacancy) VALUES (%s, %s, %s, %s, %s)''',
                        (vacancy['vacancy_name'],
                              vacancy['company_name'],
                              vacancy['salary_from'],
                              vacancy['salary_to'],
                              vacancy['url_vacancy']))
        conn.commit()
        cur.close()
        conn.close()
        return list_result







#
# obj_1 = DbSave(ApiClient.get_response_data('hh_vacancies.json'))
# result = obj_1.create_data_base('coursework_3')


# obj_1 = DbSave(ApiClient.get_response_data('hh_vacancies.json'))
# result = obj_1.create_table_company('coursework_3')
# print(result)

#
# obj_1 = DbSave(ApiClient.get_response_data('hh_vacancies.json'))
# result = obj_1.create_table_company()
# for i in result:
#     print(i)
