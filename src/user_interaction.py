import re

from src.cls_vacancy import Vacancy


def filter_vacancies(vacancies_list: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Функция возвращает результат, отфильтрованный по ключевые словам, для фильтрации вакансий"""
    return [
        vacancy
        for vacancy in vacancies_list
        for filter_word in filter_words
        if re.search(filter_word, vacancy.name, re.IGNORECASE)
        or re.search(filter_word, vacancy.snippet_requirement, re.IGNORECASE)
    ]


def get_vacancies_by_salary(filtered_vacancies: list[Vacancy], salary_range: str) -> list[Vacancy]:
    """Функция выводит диапозон зарплат от и до."""

    salary_from, salary_to = [float(salary.strip()) for salary in salary_range.split("-")]
    list_of_vacancies = []
    for vacancy in filtered_vacancies:
        if (
            salary_from <= float(vacancy.salary_from) <= salary_to
            and salary_from <= float(vacancy.salary_to) <= salary_to
        ):
            list_of_vacancies.append(vacancy)
    return list_of_vacancies


def sort_vacancies(ranged_vacancies: list[Vacancy]) -> list[Vacancy]:
    """Функция сортирует по зарплате от большего к меньшему"""
    return sorted(ranged_vacancies, key=lambda vacancy: vacancy.salary_from, reverse=True)


def get_top_vacancies(sorted_vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """функция возвращает определенное кол-во вакансий введённое пользователем"""
    return sorted_vacancies[:top_n]


def print_vacancies(top_vacancies: list[Vacancy]) -> None:
    """Функция выводит вакансии"""
    for vacancy in top_vacancies:
        print(vacancy)
