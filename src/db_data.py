import psycopg2
from dotenv import load_dotenv
import os

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.file_work import FileWork


class DbSave:
    """Класс для создания базы данных и сохранения таблиц компаний и вакансий."""

    list_vacanccies = FileWork.get_response_data("hh_vacancies.json")

    @staticmethod
    def create_data_base(name_data_base: str) -> None:
        """Создание базы данных для работы с вакансиями."""

        try:
            load_dotenv()
            password = os.getenv("db_password")
            conn = psycopg2.connect(
                user="postgres",
                password=password,
                host="localhost",
                port="5432",
                dbname="postgres",
            )
            cur = conn.cursor()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur.execute(f"""CREATE DATABASE {name_data_base}""")
            print(f"База данных: {name_data_base} успешно создана.")
        except Exception as e:
            print(f"Произошла ошибка! {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        return None

    @classmethod
    def create_table_vacancy(cls, db_name: str) -> None:
        """Метод создает таблицу вакансий в базе данных с указанием названия id вакансии,
        названия вакансии, названия компании, зарплаты и ссылки на вакансию."""

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

    @staticmethod
    def create_table_company(db_name: str) -> None:
        """Создание таблицы компании из-под таблицы вакансий."""

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
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS company (
        company_id SERIAL PRIMARY KEY,
        company_name VARCHAR(100) NOT NULL,
        count_vacancy INT NOT NULL)
            """)
            cur.execute("""
            INSERT INTO company (company_name, count_vacancy) SELECT company_name, COUNT(*) AS count_vacancy
            FROM vacancy GROUP BY company_name ORDER BY company_name ASC""")
            cur.execute("""
            ALTER TABLE vacancy ADD COLUMN company_id INT
            """)
            cur.execute("""
            UPDATE vacancy SET company_id=company.company_id FROM company\n
            WHERE vacancy.company_name=company.company_name
            """)
            cur.execute("""
            ALTER TABLE vacancy DROP COLUMN company_name
            """)
            cur.execute("""ALTER TABLE vacancy ALTER COLUMN company_id SET NOT NULL""")
            cur.execute("""
            ALTER TABLE vacancy ADD CONSTRAINT fk_list_vacancy_company_id_company
            FOREIGN KEY (company_id) REFERENCES company(company_id)
            """)
            conn.commit()
        except Exception as f:
            print(
                f"Произошла ошибка, возможно таблица уже была создана и (или) данные изменены!{f}"
            )
        finally:
            cur.close()
            conn.close()
        return None

    @staticmethod
    def exists_db(input_db_name: str) -> int:
        """Метод проверяет наличие базы данных."""

        load_dotenv()
        password = os.getenv("db_password")
        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            dbname="postgres",
        )

        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur.execute(
            """SELECT 1 FROM pg_database WHERE datname = %s""", (input_db_name,)
        )
        result = cur.fetchone()
        if result and result[0] == 1:
            print(f"База данных {input_db_name} уже существует!")
            return 1
        else:
            print(f"База данных {input_db_name} отсутствует.")
            return 0
