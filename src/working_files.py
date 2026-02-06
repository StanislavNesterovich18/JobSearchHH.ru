import json
import os
from abc import ABC, abstractmethod

from config import ROOT_DIR
from src.cls_vacancy import Vacancy


class BaseJsonSaver(ABC):
    """Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    @abstractmethod
    def open_json(self) -> None: pass

    @abstractmethod
    def save_json(self, data: list[dict]) -> None: pass

    @abstractmethod
    def add_vacancy(self, vacancies_list: list[Vacancy]) -> None: pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None: pass


class JsonSaver(BaseJsonSaver):
    """Класс для сохранения информации о вакансиях в JSON-файл."""

    __slots__ = "__filename", "data_vacancy"

    def __init__(self, filename: str = "vacancies.json") -> None:
        self.__filename = f"{ROOT_DIR}/data/{filename}"
        self.data_vacancy: list = []
        self.open_json()

    def open_json(self) -> None:
        """Функция открывает JSON файл. Если файла нет создает его"""
        if not os.path.exists(self.__filename):
            with open(self.__filename, mode="a", encoding="utf-8"):
                pass
        else:
            with open(self.__filename, mode="r", encoding="utf-8") as f:
                self.data_vacancy = json.load(f)

    def save_json(self, data: list[dict]) -> None:
        """Функция перезаписывает или добовляет в конец исходного списка информацию и сохраняет в JSON файл"""
        with open(self.__filename, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            self.data_vacancy = data

    def add_vacancy(self, vacancies_list: list[Vacancy]) -> None:
        """Функция Добовляет вакансии в список"""
        list_ids: list = [data_vacancy["id_vacancy"] for data_vacancy in self.data_vacancy]
        list_write_vacancy: list[dict] = [
            data_vacancy.to_dict() for data_vacancy in vacancies_list if data_vacancy.id_vacancy not in list_ids
        ]
        self.data_vacancy.extend(list_write_vacancy)
        self.save_json(self.data_vacancy)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Функция удаляет вакансии из списка"""
        self.data_vacancy.remove(vacancy.to_dict())
        self.save_json(self.data_vacancy)
