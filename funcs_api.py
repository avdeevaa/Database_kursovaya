from abc import ABC, abstractmethod

import requests


class GetAPI(ABC):
    """Создаем абстрактный класс
    для работы с API с вакансиями"""

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
        """Получаем информацию о вакансиях по ключевому слову"""
        self.vacancy_keyword = vacancy_keyword
        endpoint = 'employers'
        params = {'text': self.vacancy_keyword, 'only_with_vacancies': True, 'per_page': 5}

        response = requests.get(f'{self.web_url}{endpoint}', params=params)
        self.result = response.json()
        return self.result

    def get_id_employer(self):
        """Возвращает словарь с id всех работодателей, что нашлись по ключ слову,
        максимально 10 работодателей."""
        all_id = []
        for employer_id in self.result['items']:
            all_id.append(employer_id['id'])
            if len(all_id) == 9:
                break

        return all_id

    def get_vacancies_via_id(self, id_empl):
        """Получаем все вакансии работодателя через его ID"""
        self.id_empl = id_empl
        endpoint = f'vacancies?employer_id={self.id_empl}'
        params = {'per_page': 10, 'page': 1}

        response = requests.get(f'{self.web_url}{endpoint}', params=params)
        final = response.json()
        return final

# d = GetAPIhh('https://api.hh.ru/') # check code
# f = d.get_information_via_API("Сбер") # check code
#print(d.get_information_via_API("Сбер")) # check code

#print(d.get_id_employer()) # отлично, выдает нам список айди работодателей...

# sber_id = "3529"
# other_id = '829010'
# more_id = '5504955'
# m = d.get_vacancies_via_id(other_id)
#print(d.get_vacancies_via_id(sber_id))