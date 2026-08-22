import psycopg2
from dotenv import load_dotenv
import os
from decimal import Decimal
from src.file_work import FileWork


class DbManager:
    """Класс предназначен для работы с таблицами базы данных,
    в том числе обработкой и выведенийм информации о вакансиях."""


    def __init__(self, list_vacanccies=None) -> None:
        """Метод предоставляет возможность вносить свой файл при создании объекта класса"""

        if list_vacanccies == None:
            list_vacanccies = FileWork.get_response_data("hh_vacancies.json")
        else:
            self.list_vacanccies = list_vacanccies

    @classmethod
    def get_companies_and_vacancies_count(cls, db_name: str) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""

        # Устанавливаем связь с файлом .env для получения скрытых данных.
        load_dotenv()
        db_password = os.getenv("db_password")

        # Устанавливаем соединение с использованием параметров, после чего устанавливаем курсор.
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password=db_password,
            dbname=db_name,
        )
        cur = conn.cursor()

        # Демонстрируем сведения по вакансиям в каждой компании.
        cur.execute("""SELECT company_name, count_vacancy FROM company""")
        result = cur.fetchall()

        conn.commit()  # Комитим изменения в базе данных.
        cur.close()  # Закрываем курсор.
        conn.close()  # Закрываем соединение.

        # Оставил возвращение на всякий случай для возможного использования.
        return result

    @classmethod
    def get_all_vacancies(cls, db_name: str) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию."""

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
        SELECT  company.company_name, vacancy_name, salary_from, salary_to, url_vacancy FROM vacancy
        INNER JOIN company ON company.company_id=vacancy.company_id
        """)
        result = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def get_avg_salary(db_name: str) -> Decimal:
        """Получает среднюю зарплату по вакансиям."""

        load_dotenv()
        password = os.getenv("db_password")

        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            dbname=db_name,
        )
        cur = conn.cursor()
        cur.execute("""
SELECT AVG((salary_to + salary_from)/2) AS avg_salary FROM vacancy
        """)
        result = cur.fetchone()
        cur.close()
        conn.close()
        print(type(result[0]))
        return result[0]

    @classmethod
    def get_vacancies_with_higher_salary(cls, db_name: str) -> list:
        """Получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям."""

        avg_salary = DbManager.get_avg_salary(db_name)

        load_dotenv()
        password = os.getenv("db_password")

        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            dbname=db_name,
        )
        cur = conn.cursor()
        cur.execute(
            """
        SELECT * FROM vacancy WHERE ((salary_from + salary_to) / 2) > %s
        """,
            (avg_salary,),
        )
        result = cur.fetchall()

        cur.close()
        conn.close()
        return result

    @classmethod
    def get_vacancies_with_keyword(clas, db_name: str, search_word: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python."""

        load_dotenv()
        password = os.getenv("db_password")
        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            dbname=db_name,
        )
        cur = conn.cursor()
        cur.execute(
            """
        SELECT * FROM vacancy WHERE requirement ILIKE %s
        """,
            (f"%{search_word}%",),
        )

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
