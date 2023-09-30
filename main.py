from utils import *

hh_api = HeadHunterAPI()




while True:

    vacancy = input("Какую вакансию ищем? ")
    try:
        salary = int(input("Какая минимальная заплата должна быть? "))
    except ValueError:
        print("Зарплата должна быть написана только цифрами")
        continue

    if salary >= 1:
        response = hh_api.get_vacancies(vacancy, salary)
    else:
        print("Зарплата должна быть не меньше 1")
        continue

    vacancy_dict = hh_api.format_data(response)

    json_manager = JsonManager()
    json_manager.save_file(vacancy_dict)
    vacancies = json_manager.load_from_file()

    json_manager.all_vacancies(vacancies)


    print(json_manager.sort_vacancies_by_salary(vacancies))
    break

#all vac украсить цифрами
# добавить сорировку по командам