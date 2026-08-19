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

        # Создаем пустой словарь.
        dict_company = {}

        # Проходимся по списку вакинсий.
        for vacancy in self.list_vacanccies:
            # Из представленного словаря достаем наименование компании путем применения метода get.
            company_name = vacancy.get('employer', {}).get('name', {})
            # По условию если ключа(наименования компании) нет в словаре, то создается новый словарь,
            # а если компания такая уже есть, то к счетчику прибавляется 1.
            if company_name not in dict_company:
                dict_company[company_name] = 1
            else:
                dict_company[company_name] += 1

        load_dotenv()
        db_password = os.getenv('db_password')

        conn = psycopg2.connect(host='localhost', port='5432', user='postgres', password=db_password, dbname='coursework_3')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS company_vacancy 
        (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            quantity_vacancy INT NOT NULL
            
        )''')

        for key, value in dict_company.items():
            cur.execute(f'''INSERT INTO company_vacancy (company_name, quantity_vacancy) 
            VALUES (%s, %s)''', (key, value))


        conn.commit()      # Комитим изменения в базе данных.
        cur.close()        # Закрываем курсор.
        conn.close()       # Закрываем соединение.

        # Оставил возвращение на всякий случай для возможного использования.
        return dict_company












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
        return list_result










obj_1 = DBMANAGER(APICLIENT.get_response_data('hh_vacancies.json'))
result = obj_1.get_companies_and_vacancies_count()
print(result)

#
# obj_1 = DBMANAGER(APICLIENT.get_response_data('hh_vacancies.json'))
# result = obj_1.get_all_vacancies()
# for i in result:
#     print(i)