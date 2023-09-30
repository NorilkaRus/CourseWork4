import requests
import json
from abc import ABC, abstractmethod

class APIManager(ABC):

    @abstractmethod
    def get_vacancies(self, vacancy):
        """получает вакансии по апи, возвращает неформатированный json"""
        pass


    @abstractmethod
    def format_data(self):
        """
        форматирует json к единому виду "вакансии" в виде dict
        """
        pass


class JsonManager:

    def save_file(self, file):
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(file, f)

    def load_from_file(self):
        with open('vacancies.json') as f:
            text = f.read()
        text = json.loads(text)
        for key, value in text.items():
            print(key)
            print(value)

    def add_vacancy(self, vacancy):
        pass

    def get_vacancies_by_salary(self, salary):
        pass

    def delete_vacancy(self, vacancy):
        pass



class Vacancy:
    pass
    #def __init__(self, name, url, salary, ):
    # Сравнение


class HeadHunterAPI(APIManager):

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'


    def get_vacancies(self, vacancy: str, salary: int):
        """
        Получает вакансии по апи, возвращает неформатированный json
        """
        headers = {'User-Agent': 'Norilka'}
        parametres = {f'text': {vacancy},
                      'only_with_salary': True,
                      'salary': {salary}}

        response = requests.get(self.url, parametres).json()
        print(response)
        return response


    def format_data(self, data):
        """
        Приводит неформатированный JSON-словарь к единому словарю
        :param data: неформатированный JSON-словарь (результат медотода get_vacancies)
        :return: словарь с вакансиями, в котором собрана только важная информация
        """
        self.data = data
        vacancy_dict = {}

        for vacancy in data['items']:
            print(vacancy)
            vacancy_id = vacancy['id']

            # Определение зарплатной вилки и правильная запись в словарь
            if vacancy['salary']['from'] != None:
                salary_from = f"от {vacancy['salary']['from']}"
            else:
                salary_from = ""
            if vacancy['salary']['to'] != None:
                salary_to = f" до {vacancy['salary']['to']}"
            else:
                salary_to = ""

            requirement = vacancy['snippet']['requirement']
            responsibility = vacancy['snippet']['responsibility']

            vacancy_dict[vacancy_id] = {'url': f"https://hh.ru/vacancy/{vacancy_id}",
                            'name': vacancy['name'],
                            'salary': f"{salary_from}{salary_to} {vacancy['salary']['currency']}",
                            'requirement': requirement,
                            'responsibility': responsibility}

        print(vacancy_dict)
        return vacancy_dict



a = HeadHunterAPI()
b = a.get_vacancies('Python', 1) #salary не меньше 1!!

#vacancy_name = input("Какую вакансию ищем? ")
#salary = input("Размер зарплаты от: ")

w = a.format_data(b)
e = JsonManager()
e.save_file(w)
print('f')
e.load_from_file()
