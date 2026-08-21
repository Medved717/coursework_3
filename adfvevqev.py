@staticmethod
def create_data_base(name_data_base):
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
    except:
        print("База данных ")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
