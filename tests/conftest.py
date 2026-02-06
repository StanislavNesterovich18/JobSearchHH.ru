import pytest

from src.cls_vacancy import Vacancy


@pytest.fixture
def vacancy() -> Vacancy:
    return Vacancy(
        id_vacancy="123",
        name="Python Developer",
        salary_from=100000,
        salary_to=150000,
        alternate_url="https://hh.ru/vacancy/123",
        employer_id="456",
        employer_name="Company Inc.",
        snippet_requirement="Опыт работы с Python 3+",
    )


@pytest.fixture
def success_vacancy() -> Vacancy:
    return Vacancy(
        id_vacancy="123",
        name="Python Developer",
        salary_from=100000,
        salary_to=140000,
        alternate_url="https://hh.ru/vacancy/123",
        employer_id="456",
        employer_name="Company Inc.",
        snippet_requirement="Опыт работы с Python 3+",
    )


@pytest.fixture
def vacancy_wrong() -> Vacancy:
    return Vacancy(
        id_vacancy=123,  # type: ignore
        name=12333,  # type: ignore
        salary_from="100000",  # type: ignore
        salary_to="150000",  # type: ignore
        alternate_url=0,  # type: ignore
        employer_id=123,  # type: ignore
        employer_name=123,  # type: ignore
        snippet_requirement=132,  # type: ignore
    )


@pytest.fixture
def vacancies_list() -> list[Vacancy]:
    vacancy_list = [
        Vacancy(
            id_vacancy="129752860",
            name="Аналитик качества пользовательского опыта",
            salary_from=100000,
            salary_to=150000,
            alternate_url="https://hh.ru/vacancy/129752860",
            employer_id="1375441",
            employer_name="Okko",
            snippet_requirement="Знание основ математической статистики и принципов A/B-тестирования."
            "Уверенное владение SQL и <highlighttext>Python</highlighttext>."
            "Опыт построения дашбордов и визуализации метрик.",
        ),
        Vacancy(
            id_vacancy="129932011",
            name="Golang-разработчик. Nova",
            salary_from=50000,
            salary_to=90000,
            alternate_url="https://hh.ru/vacancy/129932011",
            employer_id="9329959",
            employer_name="Orion soft",
            snippet_requirement="Бэкграунд в разработке на Go более двух лет."
            "Понимание принципов работы Kubernetes и умение взаимодействовать с API + расширениями "
            "через...",
        ),
    ]
    return vacancy_list
