from _pytest.capture import CaptureFixture

from src.cls_vacancy import Vacancy
from src.user_interaction import (filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies,
                                  sort_vacancies)


def test_filter_vacancies(vacancies_list: list[Vacancy]) -> None:
    assert filter_vacancies(vacancies_list, ["Go"])[0].id_vacancy == "129932011"


def test_get_vacancies_by_salary(vacancies_list: list[Vacancy]) -> None:
    assert get_vacancies_by_salary(vacancies_list, "10000 - 1500000")[0].id_vacancy == "129752860"


def test_sort_vacancies(vacancies_list: list[Vacancy]) -> None:
    result = sort_vacancies(vacancies_list)
    assert result[0].id_vacancy == "129752860"
    assert result[1].id_vacancy == "129932011"


def test_get_top_vacancies(vacancies_list: list[Vacancy]) -> None:
    assert get_top_vacancies(vacancies_list, 1)[0].id_vacancy == "129752860"


def test_print_vacancies(capsys: CaptureFixture, vacancies_list: list[Vacancy]) -> None:
    print_vacancies(vacancies_list)
    captured = capsys.readouterr()
    assert captured.out == (
        "129752860 Аналитик качества пользовательского опыта 100000 150000 "
        "https://hh.ru/vacancy/129752860\n"
        "129932011 Golang-разработчик. Nova 50000 90000 "
        "https://hh.ru/vacancy/129932011\n"
    )
