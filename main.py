from src.cls_api_parse_hh import HH
from src.cls_vacancy import Vacancy
from src.user_interaction import (filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies,
                                  sort_vacancies)
from src.working_files import JSONSaver

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HH()
json_saver = JSONSaver()


def user_interaction() -> None:
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
    hh_vacancies = hh_api.load_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    json_saver.add_vacancy(vacancies_list)
    # json_saver.delete_vacancy(vacancies_list[0])

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
