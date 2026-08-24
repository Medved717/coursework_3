import psycopg2
from dotenv import load_dotenv
import os

from src.file_work import FileWork


class Vacancy:
    """Класс предназначен для создания таблицы vacancy в базе данных."""

    list_vacanccies = FileWork.get_response_data("hh_vacancies.json")

    @classmethod
    def create_table_vacancy(cls, db_name: str) -> None:
        """Метод создает таблицу вакансий в базе данных с указанием названия id вакансии,
        названия вакансии, названия компании, зарплаты и ссылки на вакансию."""

        cur = None
        conn = None

        try:
            list_result = []

            for vacancy in cls.list_vacanccies:
                company_name = vacancy.get("employer", {}).get("name", {})
                vacancy_name = vacancy.get("name", {})
                salary_from = vacancy.get("salary", {}).get("from", {})
                salary_to = vacancy.get("salary", {}).get("to", {})
                url_vacancy = vacancy.get("alternate_url", {})
                city_work = vacancy.get("area", {}).get("name", {})
                requirement = vacancy.get("snippet", {}).get("requirement", {})

                dict_items = {}
                dict_items["company_name"] = company_name
                dict_items["vacancy_name"] = vacancy_name
                dict_items["salary_from"] = salary_from
                dict_items["salary_to"] = salary_to
                dict_items["url_vacancy"] = url_vacancy
                dict_items["city_work"] = city_work
                dict_items["requirement"] = requirement

                list_result.append(dict_items)

            load_dotenv()
            password = os.getenv("db_password")

            conn = psycopg2.connect(
                user="postgres",
                password=password,
                port="5432",
                dbname=db_name,
                host="localhost",
            )
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancy (
                vacancy_id SERIAL PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                vacancy_name VARCHAR(100) NOT NULL,
                salary_from INT NOT NULL,
                salary_to INT NOT NULL,
                url_vacancy VARCHAR(350) NOT NULL,
                city_work VARCHAR(50) NOT NULL,
                requirement VARCHAR(350) NOT NULL
            )""")

            for vacancy in list_result:
                cur.execute(
                    """INSERT INTO vacancy (vacancy_name, company_name, salary_from, salary_to, url_vacancy,
                city_work, requirement) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        vacancy["vacancy_name"],
                        vacancy["company_name"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["url_vacancy"],
                        vacancy["city_work"],
                        vacancy["requirement"],
                    ),
                )
            conn.commit()
        except Exception as f:
            print(f"Ошибка: Возможно таблица уже была создана!{f}")
        finally:
            cur.close()
            conn.close()
        return None
