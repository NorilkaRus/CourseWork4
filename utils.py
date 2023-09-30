import requests
import json
from abc import ABC, abstractmethod
from heapq import nlargest

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


class Vacancy:
    def __init__(self, url, name, salary, requirement, responsibility):
        self.url = url
        self.name = name
        self.salary = salary
        self.requirement = requirement
        self.responsibility = responsibility

    def __repr__(self):
        return f"""{self.name}
{self.url}
{self.salary}
{self.requirement}
{self.responsibility}"""

    def salary_comparison(self):
        """
        Берет вилку зарплаты и возвращает максимальное значение
        """
        salary_list = self.salary.split(" ")
        for item in salary_list:
            if item.isalpha():
                salary_list.remove(item)
        int_lst = [int(item) for item in salary_list]
        self.max_salary = max(int_lst)
        return self.max_salary

    def __le__(self, other):
        return self.max_salary <= other.max_salary

    def __lt__(self, other):
        return self.max_salary < other.max_salary

    def __ge__(self, other):
        return self.max_salary >= other.max_salary

    def __gt__(self, other):
        return self.max_salary > other.max_salary


class JsonManager:

    def save_file(self, file):
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(file, f)

    def load_from_file(self):
        """
        Открывает файл json, считывает его и возвращает словарь с экземплярами класса Vacancy
        :return: список с экземплярами Vacancy
        """
        vacancies = []
        with open('vacancies.json') as f:
            text = f.read()
        text = json.loads(text)
        for key, value in text.items():
            vacancies.append(Vacancy(value['url'],
                                     value['name'],
                                     value['salary'],
                                     value['requirement'],
                                     value['responsibility']))
        return vacancies

    def all_vacancies(self, vacancies):
        """
        Принимает результат функции load_from_file и выводит удобный читабельный список вакансий
        :param vacancies: словарь с экземплярами класса Vacancy
        :return: удобный читабельный список вакансий в консоли
        """
        for vacancy in vacancies:
            print(f'{vacancy}\n')

    def sort_vacancies_by_salary(self, vacancies):
        """
        Принимает список вакансий, создает у каждой вакансии атрибут max_salary и возвращает красивый список
        отсрортированных по зарплате вакансий
        :param vacancies: список экземпляров Vacancy
        :return: читабельный список отсрортированных по зарплате вакансий
        """
        l = len(vacancies)
        n = 1
        for vacancy in vacancies:
            vacancy.salary_comparison()
        sorted_vacancies = nlargest(l, vacancies)
        for vacancy in sorted_vacancies:
            print(f"{n}. {vacancy}\n")
            n += 1

    def delete_vacancy(self, vacancy):
        pass


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
            vacancy_id = vacancy['id']

            # Определение зарплатной вилки и правильная запись в словарь
            if vacancy['salary']['from'] != None:
                salary_from = f"от {vacancy['salary']['from']} "
            else:
                salary_from = ""
            if vacancy['salary']['to'] != None:
                salary_to = f"до {vacancy['salary']['to']} "
            else:
                salary_to = ""

            requirement = vacancy['snippet']['requirement']
            responsibility = vacancy['snippet']['responsibility']

            vacancy_dict[vacancy_id] = {'url': f"https://hh.ru/vacancy/{vacancy_id}",
                            'name': vacancy['name'],
                            'salary': f"{salary_from}{salary_to}{vacancy['salary']['currency']}",
                            'requirement': requirement,
                            'responsibility': responsibility}

        return vacancy_dict



a = HeadHunterAPI()
b = a.get_vacancies('Python', 1) #salary не меньше 1!!
