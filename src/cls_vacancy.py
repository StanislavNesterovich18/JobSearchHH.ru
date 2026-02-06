from abc import ABC, abstractmethod
from typing import Any, Self

import f  # type: ignore


class BaseVacancy(ABC):
    """Абстрактный класс для работы с вакансиями."""

    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, hh_vacancies: list[dict]) -> list[Self]: pass

    @abstractmethod
    def __repr__(self) -> str: pass

    @abstractmethod
    def __str__(self) -> str: pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: pass


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
        self.id_vacancy = Vacancy.__validate_id_vacancy(id_vacancy)
        self.name = Vacancy.__validate_name(name)
        self.salary_from = Vacancy.__validate_salary_from(salary_from)
        self.salary_to = Vacancy.__validate_salary_to(salary_to)
        self.alternate_url = Vacancy.__validate_alternate_url(alternate_url)
        self.employer_id = Vacancy.__validate_employer_id(employer_id)
        self.employer_name = Vacancy.__validate_employer_name(employer_name)
        self.snippet_requirement = Vacancy.__validate_snippet_requirement(snippet_requirement)

    def __lt__(self, other: "Vacancy") -> Any:
        return other.salary_to < self.salary_to

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
            id_vacancy: str = f.ichain(hh_vacancy, "id") or hh_vacancy.get("id_vacancy", "Не найден")
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

    @classmethod
    def __validate_id_vacancy(cls, id_vacancy: str) -> str:
        if isinstance(id_vacancy, str) and len(id_vacancy) > 0:
            return id_vacancy
        return "Данные не указаны."

    @classmethod
    def __validate_name(cls, name: str) -> str:
        if isinstance(name, str) and len(name) > 0:
            return name
        return "Данные не указаны."

    @classmethod
    def __validate_salary_from(cls, salary_from: int) -> int:
        if isinstance(salary_from, int):
            return salary_from
        return 0

    @classmethod
    def __validate_salary_to(cls, salary_to: int) -> int:
        if isinstance(salary_to, int):
            return salary_to
        return 0

    @classmethod
    def __validate_alternate_url(cls, alternate_url: str) -> str:
        if isinstance(alternate_url, str) and len(alternate_url) > 0:
            return alternate_url
        return "Данные не указаны."

    @classmethod
    def __validate_employer_id(cls, employer_id: str) -> str:
        if isinstance(employer_id, str) and len(employer_id) > 0:
            return employer_id
        return "Данные не указаны."

    @classmethod
    def __validate_employer_name(cls, employer_name: str) -> str:
        if isinstance(employer_name, str) and len(employer_name) > 0:
            return employer_name
        return "Данные не указаны."

    @classmethod
    def __validate_snippet_requirement(cls, snippet_requirement: str) -> str:
        if isinstance(snippet_requirement, str) and len(snippet_requirement) > 0:
            return snippet_requirement
        return "Данные не указаны."
