import unittest
from unittest.mock import patch, Mock
from src.cls_api_parse_hh import HH, BaseHH


class TestHHAPI(unittest.TestCase):
    """Тесты для класса HH."""

    def test_abstract_class(self):
        """Тест на то, что BaseHH действительно абстрактный."""
        with self.assertRaises(TypeError):
            BaseHH()

    def test_hh_inheritance(self):
        """Тест на наследование от абстрактного класса."""
        hh = HH()
        self.assertIsInstance(hh, BaseHH)

    def test_hh_initialization(self):
        """Тест инициализации класса HH."""
        hh = HH()
        self.assertEqual(hh.vacancies, [])

    @patch('requests.get')
    def test_load_vacancies_success(self, mock_get):
        """Тест успешной загрузки вакансий."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Python Developer", "salary": {"from": 100000}},
                {"id": "2", "name": "Data Scientist", "salary": {"from": 120000}}
            ]
        }
        mock_get.return_value = mock_response

        hh = HH()
        vacancies = hh.load_vacancies("Python")

        self.assertEqual(len(vacancies), 2)  # 2 вакансии на двух страницах
        self.assertEqual(vacancies[0]["name"], "Python Developer")

        mock_get.assert_called()

    @patch('requests.get')
    def test_pagination_logic(self, mock_get):
        """Тест логики пагинации."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"id": "1", "name": "Test"}]}
        mock_get.return_value = mock_response

        hh = HH()
        vacancies = hh.load_vacancies("Test")

        self.assertEqual(mock_get.call_count, 1)

    def test_method_signatures(self):
        """Тест сигнатур методов."""
        hh = HH()

        self.assertTrue(hasattr(hh, 'load_vacancies'))

        import inspect
        sig = inspect.signature(hh.load_vacancies)
        self.assertEqual(str(sig), "(keyword: str) -> list[dict]")

    @patch('requests.get')
    def test_empty_response(self, mock_get):
        """Тест обработки пустого ответа."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        hh = HH()
        vacancies = hh.load_vacancies("НесуществующаяВакансия")

        self.assertEqual(len(vacancies), 0)
