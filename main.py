from utils import *

hh_api = HeadHunterAPI()
sj_api = SuperJobAPI()


while True:

    vacancy = input("Какую вакансию ищем?\n")
    while True:
        try:
            salary = int(input("Какая минимальная заплата должна быть?\n"))
        except ValueError:
            print("Зарплата должна быть написана только цифрами")
            continue

        if salary < 1:
            print("Зарплата должна быть не меньше 1")
            continue
        break

    while True:
        try:
            platform = int(input("На какой платформе искать? 1 - hh.ru, 2 - sj.ru\n"))
        except ValueError:
            print("Можно выбрать только вариант 1 или 2")
            continue
        if platform == 1:
            response = hh_api.get_vacancies(vacancy, salary)
            vacancy_dict = hh_api.format_data(response)
            break
        elif platform ==2:
            response = sj_api.get_vacancies(vacancy, salary)
            vacancy_dict = sj_api.format_data(response)
            break
        else:
            print("Можно выбрать только вариант 1 или 2")
            continue

    json_manager = JsonManager()
    json_manager.save_file(vacancy_dict)
    vacancies = json_manager.load_from_file()

    while True:
        try:
            user_input = int(input("Список вакансий сформирован.\n1. - Показать все\n2. - Отсортировать по зарплате\n"))
        except ValueError:
            print("Команда должна быть написана цифрами")
            continue

        if user_input not in [1, 2]:
            print("Неверно введена команда")
            continue
        elif user_input == 1:
            json_manager.all_vacancies(vacancies)
            break
        elif user_input == 2:
            json_manager.sort_vacancies_by_salary(vacancies)
        break

    try:
        repeat = int(input("1. - Новый поиск\n2. - Завершить\n"))
    except ValueError:
        print("Команда должна быть написана цифрами")
        continue
    if repeat == 1:
        pass
    if repeat == 2:
        break
    else:
        print("Неверно введена команда")
        continue