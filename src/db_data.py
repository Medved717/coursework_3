import psycopg2
from dotenv import load_dotenv
import os

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.file_work import FileWork


class DbSave:
    """Класс для создания базы данных и сохранения таблицы компаний"""

    @staticmethod
    def create_data_base(name_data_base: str) -> None:
        """Создание базы данных для работы с вакансиями."""

        cur = None
        conn = None

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
        company_name VARCHAR(100))
            """)
            cur.execute('''INSERT INTO company(company_name) SELECT DISTINCT(company_name) FROM vacancy ''')
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
