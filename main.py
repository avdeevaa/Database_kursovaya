from abc import ABC, abstractmethod
import json
import requests

class GetAPI(ABC):
    """Создаем абстрактный класс
    для работы с API сайтов с вакансиями"""

    @abstractmethod
    def __init__(self, web_url):
        self.web_url = web_url

    @abstractmethod
    def get_information_via_API(self, keyword):
        pass

class GetAPIhh(GetAPI):
    """Получаем вакансии из сайта HeadHunter по ключ слову, инициализируем по ссылке"""

    def __init__(self, web_url):
        super().__init__(web_url)



    def get_information_via_API(self, vacancy_keyword):

        self.vacancy_keyword = vacancy_keyword
        endpoint = 'employers'
        params = {'text': self.vacancy_keyword, 'only_with_vacancies': True, 'per_page': 5}

        response = requests.get(f'{self.web_url}{endpoint}', params=params)
        self.result = response.json()
        return self.result


    def get_id_employer(self):
        """Как мне кажется это должно возвращать словарь с
        id всех работодателей, что нашлись по ключ слову"""
        all_id = []
        for employer_id in self.result['items']:
            all_id.append(employer_id['id'])
            if len(all_id) == 9:
                break

        return all_id


    def get_info_via_id(self, id):
        """Так тут мы пытаемся прорваться к
        информации о работодателях через их айди,
        которые мы получили в предыдущей функции"""
        self.id = id

        endpoint = f'employers/{self.id}'

        response = requests.get(f'{self.web_url}{endpoint}')
        self.final = response.json()
        return self.final

    def get_vacancies_via_id(self, id_empl):
        """попробуем улучшить предыдущий код, чтобы результатом
        был просто список вакансий в понятной форме"""
        self.id_empl = id_empl
        endpoint = f'vacancies?employer_id={self.id_empl}'
        params = {'per_page': 10, 'page': 1}

        response = requests.get(f'{self.web_url}{endpoint}', params=params)
        final = response.json()
        return final
    # Это ТА САМАЯ ФУНКЦИЯ

#https://api.hh.ru/employers/{employer_id}

#vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3529'

d = GetAPIhh('https://api.hh.ru/') # check code
f = d.get_information_via_API("Сбер")
#print(d.get_information_via_API("Сбер")) # check code


#print(d.get_id_employer()) # отлично, выдает нам список айди работодателей...
# Тут нам надо поменять логику с ключевого слова на РАБОТОДАТЕЛЯ

sber_id = "3529"
other_id = '829010'
more_id = '5504955'
m = d.get_vacancies_via_id(other_id)
#print(d.get_vacancies_via_id(sber_id))







class Vacancy:
    """Класс для вакансий, инициализируется через название, ссылку, зарплату и тп."""
    def __init__(self, name, url, requirements, salary_from="не указано", salary_to="не указано", salary_currency="не указано"):
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.requirements = requirements

    def __str__(self):
      return f"""Вакансия {self.name} доступна по ссылке {self.url}.
Предлагаемая зарплата в размере от {self.salary_from} до {self.salary_to} в валюте {self.salary_currency}.
Требования: {self.requirements}"""



# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "10000", "15000", "RUB")
# vacancy1 = Vacancy("Developer", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "70000", "80000", "RUB")







class AbstractFileHandler(ABC):
    """Создаем абстрактный класс для добавления в файл"""

    @abstractmethod
    def add_vacancy(self, name):
        pass


class Vacancy_to_JSON(AbstractFileHandler):
    """Класс реализует методы добавления в файл."""

    def __init__(self, file_name): #инициализируемся по имени файла
        self.file_name = file_name


    def add_vacancy(self, name):
        self.name = name # тут мы записываем все вакансии в файл, а не по одной
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self.name, file, ensure_ascii=False, indent=4)


#check code


vac = Vacancy_to_JSON('filename.json')
vac.add_vacancy(m) # add vacancy thanks god works, and it looks beautiful, amazing!







# Получить данные о
# работодателях и их вакансиях с сайта hh.ru.
# Для этого используйте публичный API hh.ru и библиотеку
# requests

# .
# Выбрать не менее 10 интересных вам компаний, от которых вы
# будете получать данные о вакансиях по API.