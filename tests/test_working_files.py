import unittest
import json
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
from src.working_files import JsonSaver, BaseJsonSaver


class TestJsonSaver(unittest.TestCase):
    """Тесты для класса JsonBaseJsonSaverSaver."""

    def setUp(self):
        """Создаем временный файл для тестов."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_vacancies.json")

        self.vacancy1 = Mock(spec=['id_vacancy', 'to_dict'])
        self.vacancy1.id_vacancy = "123"
        self.vacancy1.to_dict.return_value = {
            "id_vacancy": "123",
            "name": "Python Developer",
            "salary_from": 100000,
            "salary_to": 150000
        }

        self.vacancy2 = Mock(spec=['id_vacancy', 'to_dict'])
        self.vacancy2.id_vacancy = "456"
        self.vacancy2.to_dict.return_value = {
            "id_vacancy": "456",
            "name": "Java Developer",
            "salary_from": 120000,
            "salary_to": 180000
        }

        self.vacancy3 = Mock(spec=['id_vacancy', 'to_dict'])
        self.vacancy3.id_vacancy = "789"
        self.vacancy3.to_dict.return_value = {
            "id_vacancy": "789",
            "name": "JavaScript Developer",
            "salary_from": 90000,
            "salary_to": 140000
        }

    def tearDown(self):
        """Удаляем временные файлы после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_abstract_class_inheritance(self):
        """Тест наследования от абстрактного класса."""
        self.assertTrue(issubclass(JsonSaver, BaseJsonSaver))

        saver = JsonSaver(self.test_file)
        self.assertIsInstance(saver, BaseJsonSaver)

    def test_init_with_new_file(self):
        """Тест инициализации с новым файлом."""
        saver = JsonSaver(self.test_file)

        self.assertEqual(saver.data_vacancy, [])
        self.assertTrue(os.path.exists(self.test_file))

    def test_init_with_existing_file(self):
        """Тест инициализации с существующим файлом."""
        initial_data = [
            {"id_vacancy": "111", "name": "Existing Vacancy"}
        ]
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False)

        saver = JsonSaver(self.test_file)

        self.assertEqual(saver.data_vacancy, initial_data)

    def test_open_json_existing_file(self):
        """Тест открытия существующего JSON файла."""
        test_data = [{"id_vacancy": "111", "name": "Test"}]
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        saver = JsonSaver(self.test_file)

        self.assertEqual(saver.data_vacancy, test_data)

    def test_open_json_corrupted_file(self):
        """Тест открытия поврежденного JSON файла."""
        # Создаем файл с некорректным JSON
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("{invalid json")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_json_write_mode(self, mock_json_dump, mock_file):
        """Тест сохранения в режиме записи (w)."""
        saver = JsonSaver(self.test_file)
        test_data = [{"id": "1"}, {"id": "2"}]

        saver.save_json(test_data, "w", overwrite=True)

        mock_file.assert_called_with(self.test_file, mode="w", encoding="utf-8")

        mock_json_dump.assert_called_once()

        self.assertEqual(saver.data_vacancy, test_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_json_append_mode(self, mock_json_dump, mock_file):
        """Тест сохранения в режиме добавления."""
        saver = JsonSaver(self.test_file)
        saver.data_vacancy = [{"id": "1"}]
        new_data = [{"id": "2"}]

        saver.save_json(new_data, "w", overwrite=False)

        self.assertEqual(len(saver.data_vacancy), 2)
        self.assertEqual(saver.data_vacancy[0], {"id": "1"})
        self.assertEqual(saver.data_vacancy[1], {"id": "2"})

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_json_without_overwrite(self, mock_json_dump, mock_file):
        """Тест сохранения без перезаписи внутренних данных."""
        saver = JsonSaver(self.test_file)
        initial_data = [{"id": "1"}]
        saver.data_vacancy = initial_data.copy()
        new_data = [{"id": "2"}]

        saver.save_json(new_data, "w", overwrite=False)

        self.assertEqual(len(saver.data_vacancy), 2)
        self.assertEqual(saver.data_vacancy[0], {"id": "1"})
        self.assertEqual(saver.data_vacancy[1], {"id": "2"})

    def test_add_vacancy_empty_list(self):
        """Тест добавления пустого списка вакансий."""
        saver = JsonSaver(self.test_file)

        initial_count = len(saver.data_vacancy)
        saver.add_vacancy([])

        self.assertEqual(len(saver.data_vacancy), initial_count)

    def test_add_vacancy_new_vacancies(self):
        """Тест добавления новых вакансий."""
        saver = JsonSaver(self.test_file)

        saver.add_vacancy([self.vacancy1])

        self.assertEqual(len(saver.data_vacancy), 1)
        self.assertEqual(saver.data_vacancy[0]["id_vacancy"], "123")

        saver.add_vacancy([self.vacancy2])

        self.assertEqual(len(saver.data_vacancy), 2)
        self.assertEqual(saver.data_vacancy[1]["id_vacancy"], "456")

    def test_add_vacancy_duplicate_vacancies(self):
        """Тест добавления дублирующихся вакансий."""
        saver = JsonSaver(self.test_file)

        saver.add_vacancy([self.vacancy1])

        initial_count = len(saver.data_vacancy)

        saver.add_vacancy([self.vacancy1])

        self.assertEqual(len(saver.data_vacancy), initial_count)

    def test_add_vacancy_multiple_vacancies(self):
        """Тест добавления нескольких вакансий одновременно."""
        saver = JsonSaver(self.test_file)

        vacancies = [self.vacancy1, self.vacancy2, self.vacancy3]
        saver.add_vacancy(vacancies)

        self.assertEqual(len(saver.data_vacancy), 3)
        self.assertEqual(saver.data_vacancy[0]["id_vacancy"], "123")
        self.assertEqual(saver.data_vacancy[1]["id_vacancy"], "456")
        self.assertEqual(saver.data_vacancy[2]["id_vacancy"], "789")

    def test_add_vacancy_mixed_duplicates(self):
        """Тест добавления вакансий с дубликатами и новыми."""
        saver = JsonSaver(self.test_file)

        saver.add_vacancy([self.vacancy1])

        saver.add_vacancy([self.vacancy1, self.vacancy2])

        self.assertEqual(len(saver.data_vacancy), 2)
        self.assertEqual(saver.data_vacancy[0]["id_vacancy"], "123")
        self.assertEqual(saver.data_vacancy[1]["id_vacancy"], "456")

    def test_delete_vacancy_existing(self):
        """Тест удаления существующей вакансии."""
        saver = JsonSaver(self.test_file)

        saver.add_vacancy([self.vacancy1, self.vacancy2, self.vacancy3])

        initial_count = len(saver.data_vacancy)

        saver.delete_vacancy(self.vacancy2)

        self.assertEqual(len(saver.data_vacancy), initial_count - 1)

        remaining_ids = [v["id_vacancy"] for v in saver.data_vacancy]
        self.assertIn("123", remaining_ids)
        self.assertNotIn("456", remaining_ids)
        self.assertIn("789", remaining_ids)
