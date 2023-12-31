import psycopg2
from database_code import config


class DBManager:
    """ класс подключается к БД PostgreSQL и возвращает методы"""
    params = config()

    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = psycopg2.connect(dbname=database_name, **DBManager.params)

    def get_companies_and_vacancies_count(self, table_name):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute(
                f'''SELECT employer_name, COUNT(vacancy_name) AS total FROM {table_name}
                GROUP BY employer_name
                ORDER BY total DESC'''
            )
            rows = cur.fetchall()
            print(f"Название компании == количество вакансий")
            for row in rows:
                employer_name, total = row
                print(f"{employer_name} -- {total}")

    def get_all_vacancies(self, table_name):
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и города."""
        with self.conn.cursor() as cur:
            cur.execute(
                f'''SELECT employer_name, vacancy_name, salary_from, currency, area_name FROM {table_name}'''
            )
            rows = cur.fetchall()
            print('Название компании == название вакансии == зарплата (если указана) == город')
            for row in rows:
                employer_name, vacancy_name, salary_from, currency, area_name = row
                print(f"{employer_name} -- {vacancy_name} -- {salary_from} {currency} -- {area_name}")

    def get_avg_salary(self, table_name):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT AVG(salary_from) FROM {table_name}"""
            )
            rows = cur.fetchone()  # выбирает первую строку!
            for row in rows:
                avg_salary = float(row)
                print(f"Средняя зарплата -- {round(avg_salary)}")

    def get_vacancies_with_higher_salary(self, table_name):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT employer_name, vacancy_name, salary_from, currency, area_name 
                FROM {table_name} WHERE salary_from > (SELECT AVG(salary_from) FROM {table_name}) 
                ORDER BY salary_from DESC"""
            )
            rows = cur.fetchall()
            print('Список вакансий, у которых зарплата выше средней.')
            print('Название компании == название вакансии == зарплата == город')
            for row in rows:
                employer_name, vacancy_name, salary_from, currency, area = row
                print(f"{employer_name} -- {vacancy_name} -- {salary_from} {currency} -- {area}")

    def get_vacancies_with_keyword(self, table_name, keyword):
        """Получает список всех вакансий, в названии которых содержится ключевое слово."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT vacancy_name, salary_from, currency, area_name, employer_name 
                FROM {table_name} WHERE vacancy_name LIKE '%{keyword}%'"""
            )
            rows = cur.fetchall()
            if cur.rowcount == 0:
                print("Нет таких вакансий.")
            else:
                print('Список вакансий, подходящих вашему ключевому слову:\n')
                for row in rows:
                    vacancy_name, salary_from, currency, area, employer_name = row
                    print(f"{vacancy_name} -- {salary_from} {currency} -- {area} -- {employer_name}")


#dbmanager = DBManager('try_dtb')
#dbmanager.get_companies_and_vacancies_count('sber') # все работает, все красиво!
#dbmanager.get_all_vacancies('sber') # все работает, все красиво!
#dbmanager.get_avg_salary('sber') # все работает
#dbmanager.get_vacancies_with_higher_salary('sber') # все работает
#dbmanager.get_vacancies_with_keyword('sber', 'менеджер') # все работает с нормальным ключевым словом
#dbmanager.get_vacancies_with_keyword('sber', 'nothing') # все работает также с неправильным ключевым словом