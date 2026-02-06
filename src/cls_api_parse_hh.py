from abc import ABC, abstractmethod

import requests
from requests import Response, Session


class BaseHH(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def load_vacancies(self, keyword: str) -> list[dict]: pass

    @abstractmethod
    def _connect(self) -> None: pass


class HH(BaseHH):
    """
    Класс для работы с API HeadHunter. Получаем список в черновом вариантре
    """

    __slots__ = (
        "__vacancies",
        "__session",
    )
    __BASE_URL: str = "https://api.hh.ru"
    __BASE_HEADERS: dict = {"User-Agent": "HH-User-Agent"}

    def __init__(self) -> None:
        self.__vacancies: list = []
        self.__session: Session = requests.Session()
        self._connect()

    def _connect(self) -> None:
        """Проверка подключения для сервиса АПИ"""
        response: Response = self.__session.get(f"{HH.__BASE_URL}", headers=HH.__BASE_HEADERS)
        print(response.url)
        response.raise_for_status()

    def load_vacancies(self, keyword: str) -> list[dict]:
        params: dict = {"text": keyword, "page": 0, "per_page": 100}

        while params.get("page") != 1:
            response: Response = self.__session.get(
                f"{HH.__BASE_URL}/vacancies", headers=HH.__BASE_HEADERS, params=params
            )
            vacancies: list = response.json()["items"]
            self.__vacancies.extend(vacancies)
            params["page"] += 1
        return self.__vacancies
