from funcs_api import GetAPIhh
from database_code import create_database, create_table_vacancy, save_vacancies_into_dtb, params
from dbman_class import DBManager


def main():

    api_init = GetAPIhh('https://api.hh.ru/')
    default_ids = ['3529', '829010', '9301808', '5504955', '2104700', '1740', '9694561', '9498120', '9498112', '5008932']  # Сбер и яндекс

    print("""Привет! Сегодня мы будем искать вакансии выбранных работодателей. 
Можно искать работодателя по ключевому слову или выбрать 10 работодателей по умолчанию.
Хотите выбрать 10 работодателей по умолчанию? (да/нет)""")
    user_answer = input().lower()
    if user_answer == "да":  # Тут мы будем использовать 10 компаний по умолчанию.
        create_database("default_companies", params)  # только один раз!!
        create_table_vacancy("default_companies", "default_vacancies", params)
        for ids in default_ids:

            save_vacancies_into_dtb(api_init.get_vacancies_via_id(ids), "default_companies", "default_vacancies", params)
        dbmanager = DBManager('default_companies')
        dbmanager.get_companies_and_vacancies_count('default_vacancies')
        user_input_1 = input('Хотите посмотреть все вакансии? (да/нет) ').lower()
        if user_input_1 == "да":
            dbmanager.get_all_vacancies('default_vacancies')
        else:
            pass
        user_input_2 = input('Хотите получить среднюю зарплату по вакансиям? (да/нет) ').lower()
        if user_input_2 == "да":
            dbmanager.get_avg_salary('default_vacancies')
        else:
            pass
        user_input_3 = input('Хотите получить список всех вакансий, у которых зарплата выше средней по всем вакансиям? (да/нет) ').lower()
        if user_input_3 == "да":
            dbmanager.get_vacancies_with_higher_salary('default_vacancies')
        else:
            pass
        user_input_4 = input('Хотите получить список всех вакансий, в названии которых содержится ключевое слово? Введите ключевое слово: ').lower()
        dbmanager.get_vacancies_with_keyword('default_vacancies', user_input_4)
        print("Спасибо за интеракцию!")

    elif user_answer == "нет":
        print("Введите ключевое слово, по которому хотите искать компании: ")
        input_keyword = input()
        create_database(f"{input_keyword}_companies", params)  # только один раз!!
        create_table_vacancy(f"{input_keyword}_companies", f"{input_keyword}_vacancies", params)

        get_info = api_init.get_information_via_API(input_keyword)
        vacancies_ids = api_init.get_id_employer()

        for ids in vacancies_ids:
            save_vacancies_into_dtb(api_init.get_vacancies_via_id(ids), f"{input_keyword}_companies", f"{input_keyword}_vacancies", params)
        dbmanager = DBManager(f"{input_keyword}_companies")
        dbmanager.get_companies_and_vacancies_count(f"{input_keyword}_vacancies")
        user_input_1 = input('Хотите посмотреть все вакансии? (да/нет) ').lower()
        if user_input_1 == "да":
            dbmanager.get_all_vacancies(f"{input_keyword}_vacancies")
        else:
            pass
        user_input_2 = input('Хотите получить среднюю зарплату по вакансиям? (да/нет) ').lower()
        if user_input_2 == "да":
            dbmanager.get_avg_salary(f"{input_keyword}_vacancies")
        else:
            pass
        user_input_3 = input(
            'Хотите получить список всех вакансий, у которых зарплата выше средней по всем вакансиям? (да/нет) ').lower()
        if user_input_3 == "да":
            dbmanager.get_vacancies_with_higher_salary(f"{input_keyword}_vacancies")
        else:
            pass
        user_input_4 = input(
            'Хотите получить список всех вакансий, в названии которых содержится ключевое слово? Введите ключевое слово: ').lower()
        dbmanager.get_vacancies_with_keyword(f"{input_keyword}_vacancies", user_input_4)
        print("Спасибо за интеракцию!")

    else:
        print("Вы не хотите искать вакансии.")

if __name__ == '__main__':
    main()
