from abc import ABC, abstractmethod
from typing import Any, Self

import f  # type: ignore


class BaseVacancy(ABC):
    """Абстрактный класс для работы с вакансиями."""

    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, hh_vacancies: list[dict]) -> list[Self]: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...


class Vacancy(BaseVacancy):
    """
    Класс для работы со списком вакансий с сайта HeadHunter.
    Обрабатываем черновой список, выбирая ключевую информацию
    """

    __slots__ = (
        "id_vacancy",
        "name",
        "salary_from",
        "salary_to",
        "alternate_url",
        "employer_id",
        "employer_name",
        "snippet_requirement",
    )

    def __init__(
        self,
        id_vacancy: str,
        name: str,
        salary_from: int,
        salary_to: int,
        alternate_url: str,
        employer_id: str,
        employer_name: str,
        snippet_requirement: str,
    ) -> None:
        self.id_vacancy = id_vacancy
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.alternate_url = alternate_url
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.snippet_requirement = snippet_requirement

    def __repr__(self) -> str:
        return f"{self.id_vacancy} {self.name} {self.salary_from} {self.salary_to} {self.alternate_url}"

    def __str__(self) -> str:
        """выводим ключевую информацию в ввиде строки"""
        return f"{self.id_vacancy} {self.name} {self.salary_from} {self.salary_to} {self.alternate_url}"

    def to_dict(self) -> dict[str, Any]:
        """Возвращаем ключевую информацию из списка"""
        return {
            "id_vacancy": self.id_vacancy,
            "name": self.name,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "alternate_url": self.alternate_url,
            "employer_id": self.employer_id,
            "employer_name": self.employer_name,
            "snippet_requirement": self.snippet_requirement,
        }

    @classmethod
    def cast_to_object_list(cls, hh_vacancies: list[dict]) -> list[Self]:
        """Возвращает список в заданом формате"""
        vacancies_list: list = []
        for hh_vacancy in hh_vacancies:
            salary_from: int = f.ichain(hh_vacancy, "salary", "from") or 0
            name: str = f.ichain(hh_vacancy, "name") or "Не найден"
            salary_to: int = f.ichain(hh_vacancy, "salary", "to") or 0
            id_vacancy: str = f.ichain(hh_vacancy, "id") or "Не найден"
            alternate_url: str = f.ichain(hh_vacancy, "alternate_url") or "Не найден"
            employer_id: str = f.ichain(hh_vacancy, "employer", "id") or "Не найден"
            employer_name: str = f.ichain(hh_vacancy, "employer", "name") or "Не найден"
            snippet_requirement: str = f.ichain(hh_vacancy, "snippet", "requirement") or "Не найден"
            vacancies_list.append(
                cls(
                    id_vacancy,
                    name,
                    salary_from,
                    salary_to,
                    alternate_url,
                    employer_id,
                    employer_name,
                    snippet_requirement,
                )
            )
        return vacancies_list
