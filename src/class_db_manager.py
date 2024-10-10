from abc import ABC, abstractmethod
from typing import Any, Dict, List

import psycopg2

from src.class_get_API import HeadHunterAPI


class ABCManagerDB(ABC):
    """Абстрактный класс поиска вакансий."""

    @abstractmethod
    def create_table(self):
        pass


class DBCreate(ABCManagerDB):
    """Класс для создания базы данных вакансий."""

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = data

    def create_table(self) -> None:
        """Функция для создания таблицы в базе данных"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute("create schema if not exists vacancies;")
            cur.execute("DROP TABLE IF EXISTS vacancies")
            cur.execute(
                "CREATE TABLE vacancies"
                "(vacancies_id int PRIMARY KEY,"
                "company_name  varchar(100) NOT NULL,"
                "vacancies_name  varchar(100) NOT NULL,"
                "salary_from  int,"
                "salary_to  int,"
                "vacancies_url  varchar NOT NULL,"
                "experience varchar(255));"
            )
            self.conn.commit()
            cur.close()
            self.conn.close()

    def insert_table(self) -> None:
        """Функция для наполнения таблицы данными с API HH.ru"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            count = 1
            for item in self.data:
                if item.get("salary") is None:
                    cur.execute(
                        "INSERT INTO vacancies (vacancies_id, company_name, vacancies_name, "
                        "salary_from, salary_to, vacancies_url, experience) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            count,
                            item.get("employer").get("name"),
                            item.get("name"),
                            item.get("salary"),
                            item.get("salary"),
                            item.get("alternate_url"),
                            item.get("experience").get("name"),
                        ),
                    )
                else:
                    cur.execute(
                        "INSERT INTO vacancies (vacancies_id, company_name, vacancies_name, "
                        "salary_from, salary_to, vacancies_url, experience) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            count,
                            item.get("employer").get("name"),
                            item.get("name"),
                            item.get("salary").get("from"),
                            item.get("salary").get("to"),
                            item.get("alternate_url"),
                            item.get("experience").get("name"),
                        ),
                    )
                count += 1
            self.conn.commit()
            cur.close()
            self.conn.close()

    def connect_data_base(self):
        """Функция для создания подключения к базе данных"""
        self.conn = psycopg2.connect(host="", database="", user="", password="")


hh_api = HeadHunterAPI("Детский мир")
s = hh_api.get_vacancies_from_employer_id()
cadc = DBCreate(s)
cadc.create_table()
cadc.insert_table()
