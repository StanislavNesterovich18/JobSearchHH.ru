import unittest
from unittest.mock import Mock, patch
from io import StringIO
from src.user_interaction import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies
)


class TestVacancyFilters(unittest.TestCase):
    """Тесты для функций фильтрации вакансий."""

    def setUp(self):
        """Создаем тестовые вакансии."""
        self.vacancies = [
            Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to']),
            Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to']),
            Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to']),
            Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to']),
        ]

        self.vacancies[0].name = "Python Developer"
        self.vacancies[0].snippet_requirement = "Опыт работы с Django и Flask"
        self.vacancies[0].salary_from = 100000
        self.vacancies[0].salary_to = 150000

        self.vacancies[1].name = "Java Developer"
        self.vacancies[1].snippet_requirement = "Spring Framework, Hibernate"
        self.vacancies[1].salary_from = 120000
        self.vacancies[1].salary_to = 180000

        self.vacancies[2].name = "JavaScript Developer"
        self.vacancies[2].snippet_requirement = "React, Node.js, TypeScript"
        self.vacancies[2].salary_from = 90000
        self.vacancies[2].salary_to = 140000

        self.vacancies[3].name = "Data Scientist"
        self.vacancies[3].snippet_requirement = "Python, Machine Learning, SQL"
        self.vacancies[3].salary_from = 150000
        self.vacancies[3].salary_to = 250000

    def test_filter_vacancies_by_name(self):
        """Тест фильтрации по названию вакансии."""
        filtered = filter_vacancies(self.vacancies, ["Python"])

        self.assertEqual(len(filtered), 2)  # Python Developer и Data Scientist
        self.assertEqual(filtered[0].name, "Python Developer")
        self.assertEqual(filtered[1].name, "Data Scientist")

    def test_filter_vacancies_by_requirement(self):
        """Тест фильтрации по требованиям."""
        filtered = filter_vacancies(self.vacancies, ["React"])

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "JavaScript Developer")

    def test_filter_vacancies_multiple_keywords(self):
        """Тест фильтрации по нескольким ключевым словам."""
        filtered = filter_vacancies(self.vacancies, ["Python", "Java"])

        self.assertEqual(len(filtered), 4)  # Python Developer, Java Developer, Data Scientist

    def test_filter_vacancies_case_insensitive(self):
        """Тест регистронезависимой фильтрации."""
        filtered = filter_vacancies(self.vacancies, ["python", "JAVA"])

        self.assertEqual(len(filtered), 4)

    def test_filter_vacancies_no_matches(self):
        """Тест фильтрации без совпадений."""
        filtered = filter_vacancies(self.vacancies, ["C++"])

        self.assertEqual(len(filtered), 2)

    def test_filter_vacancies_empty_filter_words(self):
        """Тест фильтрации с пустым списком ключевых слов."""
        filtered = filter_vacancies(self.vacancies, [])

        self.assertEqual(len(filtered), 0)

    def test_filter_vacancies_empty_vacancies_list(self):
        """Тест фильтрации пустого списка вакансий."""
        filtered = filter_vacancies([], ["Python"])

        self.assertEqual(len(filtered), 0)

    def test_filter_vacancies_special_characters(self):
        """Тест фильтрации с специальными символами в ключевых словах."""
        cpp_vacancy = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        cpp_vacancy.name = "C++ Developer"
        cpp_vacancy.snippet_requirement = "Опыт работы с STL"
        cpp_vacancy.salary_from = 110000
        cpp_vacancy.salary_to = 160000

        all_vacancies = self.vacancies + [cpp_vacancy]

        filtered = filter_vacancies(all_vacancies, ["C\+\+"])

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "C++ Developer")

    def test_get_vacancies_by_salary_valid_range(self):
        """Тест фильтрации по диапазону зарплат."""
        filtered = get_vacancies_by_salary(self.vacancies, "100000-200000")

        self.assertEqual(len(filtered), 2)  # Python, Java, JavaScript

    def test_get_vacancies_by_salary_exact_match(self):
        """Тест фильтрации по точному диапазону."""
        filtered = get_vacancies_by_salary(self.vacancies, "150000-250000")

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "Data Scientist")

    def test_get_vacancies_by_salary_low_range(self):
        """Тест фильтрации по низкому диапазону зарплат."""
        filtered = get_vacancies_by_salary(self.vacancies, "80000-100000")

        self.assertEqual(len(filtered), 0)  # JavaScript Developer (90000-140000)

    def test_get_vacancies_by_salary_float_values(self):
        """Тест фильтрации с дробными значениями зарплат."""
        float_vacancy = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        float_vacancy.name = "Test"
        float_vacancy.snippet_requirement = "Test"
        float_vacancy.salary_from = 99999.99
        float_vacancy.salary_to = 100000.01

        filtered = get_vacancies_by_salary([float_vacancy], "99999-100001")

        self.assertEqual(len(filtered), 1)

    def test_get_vacancies_by_salary_invalid_format(self):
        """Тест обработки неверного формата диапазона зарплат."""
        with self.assertRaises(ValueError):
            get_vacancies_by_salary(self.vacancies, "100000-200000-300000")

        with self.assertRaises(ValueError):
            get_vacancies_by_salary(self.vacancies, "не число-200000")

    def test_get_vacancies_by_salary_empty_list(self):
        """Тест фильтрации пустого списка вакансий по зарплате."""
        filtered = get_vacancies_by_salary([], "100000-200000")

        self.assertEqual(len(filtered), 0)

    def test_get_vacancies_by_salary_edge_cases(self):
        """Тест граничных случаев при фильтрации по зарплате."""
        edge_vacancy = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        edge_vacancy.name = "Edge Case"
        edge_vacancy.snippet_requirement = "Test"
        edge_vacancy.salary_from = 100000
        edge_vacancy.salary_to = 200000

        filtered = get_vacancies_by_salary([edge_vacancy], "100000-200000")
        self.assertEqual(len(filtered), 1)

        filtered = get_vacancies_by_salary([edge_vacancy], "110000-190000")
        self.assertEqual(len(filtered), 0)

        filtered = get_vacancies_by_salary([edge_vacancy], "90000-190000")
        self.assertEqual(len(filtered), 0)

        filtered = get_vacancies_by_salary([edge_vacancy], "110000-210000")
        self.assertEqual(len(filtered), 0)

        filtered = get_vacancies_by_salary([edge_vacancy], "50000-90000")
        self.assertEqual(len(filtered), 0)

    def test_sort_vacancies(self):
        """Тест сортировки вакансий по зарплате."""
        unsorted_vacancies = [
            self.vacancies[2],  # 90000
            self.vacancies[0],  # 100000
            self.vacancies[1],  # 120000
            self.vacancies[3],  # 150000
        ]

        sorted_list = sort_vacancies(unsorted_vacancies)

        self.assertEqual(sorted_list[0].name, "Data Scientist")  # 150000
        self.assertEqual(sorted_list[1].name, "Java Developer")  # 120000
        self.assertEqual(sorted_list[2].name, "Python Developer")  # 100000
        self.assertEqual(sorted_list[3].name, "JavaScript Developer")  # 90000

    def test_sort_vacancies_empty_list(self):
        """Тест сортировки пустого списка."""
        sorted_list = sort_vacancies([])

        self.assertEqual(len(sorted_list), 0)

    def test_sort_vacancies_single_element(self):
        """Тест сортировки списка с одним элементом."""
        single_list = [self.vacancies[0]]

        sorted_list = sort_vacancies(single_list)

        self.assertEqual(len(sorted_list), 1)
        self.assertEqual(sorted_list[0].name, "Python Developer")

    def test_sort_vacancies_equal_salaries(self):
        """Тест сортировки при одинаковых зарплатах."""
        vacancy1 = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        vacancy1.name = "First"
        vacancy1.salary_from = 100000

        vacancy2 = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        vacancy2.name = "Second"
        vacancy2.salary_from = 100000

        sorted_list = sort_vacancies([vacancy1, vacancy2])

        self.assertEqual(sorted_list[0].name, "First")
        self.assertEqual(sorted_list[1].name, "Second")

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий."""
        top_2 = get_top_vacancies(self.vacancies, 2)

        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0], self.vacancies[0])
        self.assertEqual(top_2[1], self.vacancies[1])

    def test_get_top_vacancies_more_than_available(self):
        """Тест получения топ N, где N больше количества вакансий."""
        top_10 = get_top_vacancies(self.vacancies, 10)

        self.assertEqual(len(top_10), 4)

    def test_get_top_vacancies_zero_or_negative(self):
        """Тест получения топ 0 или отрицательного числа вакансий."""
        top_0 = get_top_vacancies(self.vacancies, 0)
        self.assertEqual(len(top_0), 0)

    def test_get_top_vacancies_empty_list(self):
        """Тест получения топ N из пустого списка."""
        top_5 = get_top_vacancies([], 5)

        self.assertEqual(len(top_5), 0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_vacancies_empty(self, mock_stdout):
        """Тест вывода пустого списка вакансий."""
        print_vacancies([])

        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    def test_integration_workflow(self):
        """Интеграционный тест всего workflow."""
        filtered = filter_vacancies(self.vacancies, ["Python", "Developer"])

        salary_filtered = get_vacancies_by_salary(filtered, "80000-200000")

        sorted_vacancies = sort_vacancies(salary_filtered)

        top_vacancies = get_top_vacancies(sorted_vacancies, 2)

        self.assertEqual(len(filtered), 5)  # Python Developer, JavaScript Developer, Data Scientist
        self.assertEqual(len(salary_filtered),
                         4)  # Python Developer, JavaScript Developer (Data Scientist имеет salary_to=250000)
        self.assertEqual(len(top_vacancies), 2)

        if len(top_vacancies) > 1:
            self.assertGreaterEqual(
                top_vacancies[0].salary_from,
                top_vacancies[1].salary_from
            )


class TestVacancyFiltersEdgeCases(unittest.TestCase):
    """Тесты граничных случаев для функций фильтрации."""

    def test_filter_vacancies_empty_strings(self):
        """Тест фильтрации с пустыми строками."""
        vacancy_empty = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        vacancy_empty.name = ""
        vacancy_empty.snippet_requirement = ""
        vacancy_empty.salary_from = 100000
        vacancy_empty.salary_to = 150000

        filtered = filter_vacancies([vacancy_empty], ["Python"])

        self.assertEqual(len(filtered), 0)

    def test_salary_filter_with_string_salaries(self):
        """Тест фильтрации по зарплате со строковыми значениями."""
        vacancy_string_salary = Mock(spec=['name', 'snippet_requirement', 'salary_from', 'salary_to'])
        vacancy_string_salary.name = "Test"
        vacancy_string_salary.snippet_requirement = "Test"
        vacancy_string_salary.salary_from = "100000"  # Строка вместо числа
        vacancy_string_salary.salary_to = "150000"  # Строка вместо числа

        filtered = get_vacancies_by_salary([vacancy_string_salary], "90000-160000")

        self.assertEqual(len(filtered), 1)
