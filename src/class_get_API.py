from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class ABCParser(ABC):
    """Абстрактный класс поиска вакансий."""

    @abstractmethod
    def get_vacancies(self):
        pass


class ParserHH(ABCParser):
    """Базовый класс поиска вакансий с HH.ru"""

    search_text: str

    def __init__(self, search_text: str) -> None:
        if type(search_text) is str:
            self.search_text = search_text
        else:
            raise TypeError("Текст поиска должен быть 'str'")
        self.url = "https://api.hh.ru/vacancies"
        self.params = {"text": self.search_text, "per_page": 30, "page": 0}

    def __get_vacancies(self):
        """Функция поиска вакансий по API"""
        try:
            response = requests.get(self.url, self.params, timeout=5)
            verified_response = self._response_status_code(response)
            vacancies_data = verified_response.json()["items"]
            return vacancies_data
        except AttributeError:
            print("Произошла ошибка.")

    def _response_status_code(self, response):
        """Метод проверки API на ошибки
        :param response: Ответ от HH.ru
        :return: Ответ от HH.ru без ошибок
        """
        try:
            if response.status_code == 200:
                return response
        except requests.exceptions.Timeout:
            print("Время ожидания запроса истекло. Пожалуйста, проверьте свое интернет-соединение.")
        except requests.exceptions.RequestException:
            print("Произошла ошибка. Пожалуйста, повторите попытку позже.")
        else:
            print("Запрос не был успешным.")

    @property
    def get_vacancies(self) -> List[Dict[str, Any]]:
        """Функция вывода вакансий найденых по API"""
        return self.__get_vacancies()


class HeadHunterAPI(ParserHH):
    """Класс поиска вакансий с HH.ru по компании"""

    search_text: str

    def __init__(self, search_text: str) -> None:
        super().__init__(search_text)
        self.url_employer_id = "https://api.hh.ru/employers"
        self.params_employer_id = {"text": self.search_text}

    def __get_employer_id(self):
        """Функция получения id компании"""
        try:
            response = requests.get(self.url_employer_id, self.params_employer_id, timeout=5)
            verified_response = self._response_status_code(response)
            vacancies_data = verified_response.json()["items"]
            return vacancies_data
        except AttributeError:
            print("Произошла ошибка.")

    def __get_employer_list_id(self) -> List[Dict[str, Any]]:
        """Функция получения информации о компаниях"""
        self.list_id = []
        response_employer_id = self.__get_employer_id()
        for employer_id in response_employer_id:
            self.list_id.append(employer_id["id"])
        return self.list_id

    def get_vacancies_from_employer_id(self) -> list:
        """Функция получения вакансий из списка id компаний"""
        list_d = []
        for emp_id in self.__get_employer_list_id():
            self.params = {"employer_id": emp_id, "per_page": 100}
            list_d.extend(self.get_vacancies)
        return list_d

    @property
    def get_employer_list_id(self):
        """Функция вывода списка id найденых компаний"""
        return self.__get_employer_list_id()
