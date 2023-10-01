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

    #все
    json_manager.all_vacancies(vacancies)

    #сортировка
    json_manager.sort_vacancies_by_salary(vacancies)
    break


# добавить сорировку по командам
#очистка json
# начать заново