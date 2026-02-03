import unittest
from src.cls_vacancy import Vacancy, BaseVacancy


class TestVacancy(unittest.TestCase):
    """Тесты для класса Vacancy."""

    def test_abstract_class_inheritance(self):
        """Тест наследования от абстрактного класса."""
        self.assertTrue(issubclass(Vacancy, BaseVacancy))

        vacancy = Vacancy(
            id_vacancy="123",
            name="Python Developer",
            salary_from=100000,
            salary_to=150000,
            alternate_url="https://hh.ru/vacancy/123",
            employer_id="456",
            employer_name="Company Inc.",
            snippet_requirement="Опыт работы с Python 3+"
        )
        self.assertIsInstance(vacancy, BaseVacancy)

    def test_init_and_attributes(self):
        """Тест инициализации и атрибутов."""
        vacancy = Vacancy(
            id_vacancy="123",
            name="Python Developer",
            salary_from=100000,
            salary_to=150000,
            alternate_url="https://hh.ru/vacancy/123",
            employer_id="456",
            employer_name="Company Inc.",
            snippet_requirement="Опыт работы с Python 3+"
        )

        self.assertEqual(vacancy.id_vacancy, "123")
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.alternate_url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.employer_id, "456")
        self.assertEqual(vacancy.employer_name, "Company Inc.")
        self.assertEqual(vacancy.snippet_requirement, "Опыт работы с Python 3+")

        self.assertEqual(vacancy.__slots__, (
            "id_vacancy",
            "name",
            "salary_from",
            "salary_to",
            "alternate_url",
            "employer_id",
            "employer_name",
            "snippet_requirement",
        ))

    def test_repr_method(self):
        """Тест метода __repr__."""
        vacancy = Vacancy(
            id_vacancy="123",
            name="Python Developer",
            salary_from=100000,
            salary_to=150000,
            alternate_url="https://hh.ru/vacancy/123",
            employer_id="456",
            employer_name="Company Inc.",
            snippet_requirement="Требования..."
        )

        expected_repr = "123 Python Developer 100000 150000 https://hh.ru/vacancy/123"
        self.assertEqual(repr(vacancy), expected_repr)

    def test_str_method(self):
        """Тест метода __str__."""
        vacancy = Vacancy(
            id_vacancy="123",
            name="Python Developer",
            salary_from=100000,
            salary_to=150000,
            alternate_url="https://hh.ru/vacancy/123",
            employer_id="456",
            employer_name="Company Inc.",
            snippet_requirement="Требования..."
        )

        expected_str = "123 Python Developer 100000 150000 https://hh.ru/vacancy/123"
        self.assertEqual(str(vacancy), expected_str)

    def test_to_dict_method(self):
        """Тест метода to_dict()."""
        vacancy = Vacancy(
            id_vacancy="123",
            name="Python Developer",
            salary_from=100000,
            salary_to=150000,
            alternate_url="https://hh.ru/vacancy/123",
            employer_id="456",
            employer_name="Company Inc.",
            snippet_requirement="Опыт работы с Python 3+"
        )

        result = vacancy.to_dict()

        self.assertIsInstance(result, dict)

        expected_keys = {
            "id_vacancy", "name", "salary_from", "salary_to",
            "alternate_url", "employer_id", "employer_name", "snippet_requirement"
        }
        self.assertEqual(set(result.keys()), expected_keys)

        self.assertEqual(result["id_vacancy"], "123")
        self.assertEqual(result["name"], "Python Developer")
        self.assertEqual(result["salary_from"], 100000)
        self.assertEqual(result["salary_to"], 150000)
        self.assertEqual(result["alternate_url"], "https://hh.ru/vacancy/123")
        self.assertEqual(result["employer_id"], "456")
        self.assertEqual(result["employer_name"], "Company Inc.")
        self.assertEqual(result["snippet_requirement"], "Опыт работы с Python 3+")

    def test_cast_to_object_list_single_vacancy(self):
        """Тест преобразования одной вакансии."""
        hh_vacancy = {
            "id": "123",
            "name": "Python Developer",
            "salary": {
                "from": 100000,
                "to": 150000,
                "currency": "RUR"
            },
            "alternate_url": "https://hh.ru/vacancy/123",
            "employer": {
                "id": "456",
                "name": "Company Inc."
            },
            "snippet": {
                "requirement": "Опыт работы с Python 3+"
            }
        }

        vacancies = Vacancy.cast_to_object_list([hh_vacancy])

        self.assertEqual(len(vacancies), 1)

        vacancy = vacancies[0]
        self.assertEqual(vacancy.id_vacancy, "123")
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.alternate_url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.employer_id, "456")
        self.assertEqual(vacancy.employer_name, "Company Inc.")
        self.assertEqual(vacancy.snippet_requirement, "Опыт работы с Python 3+")

    def test_cast_to_object_list_multiple_vacancies(self):
        """Тест преобразования нескольких вакансий."""
        hh_vacancies = [
            {
                "id": "1",
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000},
                "alternate_url": "https://hh.ru/vacancy/1",
                "employer": {"id": "10", "name": "Company A"},
                "snippet": {"requirement": "Python 3+"}
            },
            {
                "id": "2",
                "name": "Java Developer",
                "salary": {"from": 120000, "to": 180000},
                "alternate_url": "https://hh.ru/vacancy/2",
                "employer": {"id": "20", "name": "Company B"},
                "snippet": {"requirement": "Java 8+"}
            }
        ]

        vacancies = Vacancy.cast_to_object_list(hh_vacancies)

        self.assertEqual(len(vacancies), 2)

        self.assertEqual(vacancies[0].id_vacancy, "1")
        self.assertEqual(vacancies[0].name, "Python Developer")
        self.assertEqual(vacancies[0].salary_from, 100000)

        self.assertEqual(vacancies[1].id_vacancy, "2")
        self.assertEqual(vacancies[1].name, "Java Developer")
        self.assertEqual(vacancies[1].salary_from, 120000)

    def test_cast_to_object_list_missing_fields(self):
        """Тест обработки вакансий с отсутствующими полями."""
        hh_vacancy = {
            "id": "123",
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "employer": {
                "id": "456",
                "name": "Company Inc."
            },
            "snippet": {
                "requirement": None
            }
        }

        vacancies = Vacancy.cast_to_object_list([hh_vacancy])

        vacancy = vacancies[0]
        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)
        self.assertEqual(vacancy.snippet_requirement, "Не найден")

    def test_cast_to_object_list_empty_list(self):
        """Тест преобразования пустого списка."""
        vacancies = Vacancy.cast_to_object_list([])
        self.assertEqual(vacancies, [])
        self.assertIsInstance(vacancies, list)

    def test_zero_salary(self):
        """Тест работы с нулевой зарплатой."""
        vacancy = Vacancy(
            id_vacancy="123",
            name="Intern",
            salary_from=0,
            salary_to=0,
            alternate_url="https://hh.ru/vacancy/123",
            employer_id="456",
            employer_name="Company Inc.",
            snippet_requirement="Обучение"
        )

        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)

        result = vacancy.to_dict()
        self.assertEqual(result["salary_from"], 0)
        self.assertEqual(result["salary_to"], 0)
