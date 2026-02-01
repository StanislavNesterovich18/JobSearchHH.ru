from abc import ABC, abstractmethod

import requests
from requests import Response


class BaseHH(ABC):
    @abstractmethod
    def load_vacancies(self, keyword: str) -> list[dict]: ...


class HH(BaseHH):
    """
    Класс для работы с API HeadHunter
    """

    __BASE_URL: str = "https://api.hh.ru"
    __BASE_HEADERS: dict = {"User-Agent": "HH-User-Agent"}

    def __init__(self) -> None:
        self.vacancies: list = []

    def load_vacancies(self, keyword: str) -> list[dict]:
        params: dict = {"text": keyword, "page": 0, "per_page": 100}
        while params.get("page") != 1:
            response: Response = requests.get(f"{HH.__BASE_URL}/vacancies", headers=HH.__BASE_HEADERS, params=params)
            vacancies: list = response.json()["items"]
            self.vacancies.extend(vacancies)
            params["page"] += 1
        return self.vacancies


if __name__ == "__main__":
    hh = HH()
    hh.load_vacancies("python")
    print(hh.vacancies)
