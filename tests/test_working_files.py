import json
import os
from unittest.mock import mock_open, patch

from config import ROOT_DIR
from src.cls_vacancy import Vacancy
from src.working_files import JsonSaver


def test_working_files(vacancies_list: list[Vacancy]) -> None:
    jsonsaver: JsonSaver = JsonSaver(filename="test_working_files.json")
    convert_str = json.dumps(vacancies_list[0].to_dict())
    with patch("os.path.exists") as exists_mock:
        exists_mock.return_value = False
        dict_vacancy = [vacancies_list[0].to_dict()]
        jsonsaver.save_json(dict_vacancy)

    json_saver: JsonSaver = JsonSaver(filename="test_working_files.json")
    with patch("os.path.exists") as exists_mock:
        exists_mock.return_value = True
        with patch("builtins.open", mock_open(read_data=convert_str)):
            assert json_saver.data_vacancy[0]["id_vacancy"] == vacancies_list[0].id_vacancy
    json_saver.add_vacancy(vacancies_list)
    json_saver.delete_vacancy(vacancies_list[1])
    os.remove(f"{ROOT_DIR}/data/test_working_files.json")
