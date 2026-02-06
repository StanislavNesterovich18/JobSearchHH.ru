from src.cls_vacancy import Vacancy


def test_vacancy(vacancy: Vacancy, success_vacancy: Vacancy, vacancy_wrong: Vacancy) -> None:

    assert Vacancy.cast_to_object_list([vacancy.to_dict()])[0].id_vacancy == "123"
    assert vacancy.id_vacancy == "123"
    assert vacancy_wrong.id_vacancy == "Данные не указаны."
    assert repr(vacancy) == "123 Python Developer 100000 150000 https://hh.ru/vacancy/123"
    assert str(vacancy) == "123 Python Developer 100000 150000 https://hh.ru/vacancy/123"
    assert vacancy.to_dict() == {
        "alternate_url": "https://hh.ru/vacancy/123",
        "employer_id": "456",
        "employer_name": "Company Inc.",
        "id_vacancy": "123",
        "name": "Python Developer",
        "salary_from": 100000,
        "salary_to": 150000,
        "snippet_requirement": "Опыт работы с Python 3+",
    }
    assert vacancy < success_vacancy
