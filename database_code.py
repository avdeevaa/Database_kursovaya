import psycopg2
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def create_database(database_name: str, params):
    """Создаем базу данных, в которой будет лежать информация о таблицах"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()


def create_table_vacancy(database_name, table_name, params):
    """Создаем таблицу в базе данных"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(100) NOT NULL,
                area_name VARCHAR(60),
                salary_from INT,
                currency VARCHAR(3),
                employer_id VARCHAR(15),
                employer_name VARCHAR(40),
                requirements TEXT
            )
        """)

    conn.commit()
    conn.close()


params = config()
#create_database("try_dtb", params) #dtb was created
#create_table_vacancy("try_dtb", "SBER", params) #table was also created


def save_vacancies_into_dtb(data, database_name, table_name, params):
    """Заполняем таблицу информацией из АПИ."""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for item in data['items']:
            vacancy_name = item['name']
            area_name = item['area']['name']
            try:
                salary_from = item['salary']['from']

                if salary_from is None:
                    salary_from = 0
            except TypeError:
                continue
            try:
                currency = item['salary']['currency']
                if currency is None:
                    currency = "RUB"
            except TypeError:
                continue

            employer_id = item['employer']['id']
            employer_name = item['employer']['name']
            requirements = item['snippet']['requirement']

            cur.execute(
                f"""
                INSERT INTO {table_name} (vacancy_name, area_name, salary_from, currency, employer_id, 
                employer_name, requirements) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    vacancy_name, area_name, salary_from, currency,
                    employer_id, employer_name, requirements
                )
            )
    conn.commit()
    conn.close()


#from funcs_api import m
#save_vacancies_into_dtb(m, "try_dtb", "SBER", params)
# it works, table is OK, work for all vacancies
