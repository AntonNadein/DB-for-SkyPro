from abc import ABC, abstractmethod
from typing import Any, Dict, List
from dotenv import load_dotenv

import psycopg2
import os


class ABCDataBase(ABC):
    """Абстрактный класс для базы данных."""

    @abstractmethod
    def connect_data_base(self):
        pass


class DataBase(ABCDataBase):
    """Класс для подключения к базе данных."""

    def __init__(self):
        load_dotenv()
        self.host = os.getenv("DATABASE_HOST")
        self.database = os.getenv("DATABASE_NAME")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.port = 5432

    def connect_data_base(self) -> None:
        """Функция для создания подключения к базе данных"""
        self.conn = psycopg2.connect(host=self.host,
                                     database=self.database,
                                     user=self.user,
                                     password=self.password,
                                     port=self.port)


class DBCreate(DataBase):
    """Класс для создания базы данных вакансий."""

    data: List[Dict[str, Any]]

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        super().__init__()
        self.data = data

    def create_table(self) -> None:
        """Функция для создания таблицы в базе данных"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute("create schema if not exists vacancies;")
            cur.execute("DROP TABLE IF EXISTS vacancies")
            cur.execute(
                "CREATE TABLE vacancies"
                "(vacancies_id serial PRIMARY KEY,"
                "company_name  varchar(100) NOT NULL,"
                "vacancies_name  varchar(100) NOT NULL,"
                "salary_from  int,"
                "salary_to  int,"
                "vacancies_url  varchar NOT NULL);"
            )
            self.conn.commit()
            cur.close()
            self.conn.close()

    def insert_table(self) -> None:
        """Функция для наполнения таблицы данными с API HH.ru"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            for item in self.data:
                if item.get("salary") is None:
                    cur.execute(
                        "INSERT INTO vacancies (company_name, vacancies_name, "
                        "salary_from, salary_to, vacancies_url) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (
                            item.get("employer").get("name"),
                            item.get("name"),
                            item.get("salary"),
                            item.get("salary"),
                            item.get("alternate_url")
                        ),
                    )
                else:
                    cur.execute(
                        "INSERT INTO vacancies (company_name, vacancies_name, "
                        "salary_from, salary_to, vacancies_url) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (
                            item.get("employer").get("name"),
                            item.get("name"),
                            item.get("salary").get("from"),
                            item.get("salary").get("to"),
                            item.get("alternate_url")
                        ),
                    )
            self.conn.commit()
            cur.close()
            self.conn.close()


class DBManager(DataBase):
    """Класс взаимодействия с базой данных вакансий."""

    def get_companies_and_vacancies_count(self) -> None:
        """Функция возвращает список всех компаний и
        количество вакансий у каждой компании"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute("SELECT company_name, COUNT(*) FROM vacancies GROUP BY company_name")

            rows = cur.fetchall()
            print("Список всех компаний и количество вакансий у каждой компании")
            print("--- " * 15)
            for row in rows:
                print(f"Компания: {row[0]} " f"Вакансий: {row[1]}")

            cur.close()
            self.conn.close()

    def get_all_vacancies(self) -> None:
        """Функция возвращает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute("SELECT company_name, vacancies_name, salary_from, salary_to, vacancies_url FROM vacancies")

            rows = cur.fetchall()
            print("Список всех вакансий")
            print("--- " * 15)
            for row in rows:
                if row[2] is None and row[3] is None:
                    salary = "Зарплата не указана"
                elif type(row[2]) is int and row[3] is None:
                    salary = f"Зарплата от {row[2]}"
                elif row[2] is None and type(row[3]) is int:
                    salary = f"Зарплата до {row[3]}"
                else:
                    salary = f"Зарплата от {row[2]} до {row[3]}"
                print(f"Компания: {row[0]} " f"Количаство вакансий: {row[1]} " f"{salary} " f"URL: {row[4]} ")

            cur.close()
            self.conn.close()

    def get_avg_salary(self) -> None:
        """Функция возвращает среднюю зарплату по вакансиям"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT vacancies_name, (avg(salary_from) + avg(salary_to))/2 as avg_salary "
                "FROM vacancies "
                "GROUP BY vacancies_name "
                "HAVING (avg(salary_from) is not null and avg(salary_to) is not null)"
            )
            rows = cur.fetchall()
            print("Средняя зарплата по вакансиям")
            print("--- " * 15)
            for row in rows:
                print(f"Вакансия: {row[0]} " f"Средняя зарплата: {round(row[1])}")

            cur.close()
            self.conn.close()

    def get_vacancies_with_higher_salary(self) -> None:
        """Функция возвращает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM vacancies "
                "WHERE (salary_from + salary_to)/2 > "
                "(SELECT (avg(salary_from) + avg(salary_to))/2 as avg_salary FROM vacancies)"
            )

            rows = cur.fetchall()
            print("Вакансии у которых зарплата выше средней по всем вакансиям")
            print("--- " * 15)
            for row in rows:
                print(
                    f"Компания: {row[1]} "
                    f"Вакансия: {row[2]} "
                    f"Зарплата от {row[3]} до {row[4]} "
                    f"URL: {row[5]} "
                )

            cur.close()
            self.conn.close()

    def get_vacancies_with_keyword(self, input_text: str) -> None:
        """Функция поиска по шаблону, возвращает список всех вакансий,
        в названии которых содержатся переданные в метод слова"""
        self.connect_data_base()
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies " f" WHERE vacancies_name LIKE '%{input_text}%'")

            rows = cur.fetchall()
            print(f'Вакансии в названии которых содержатся "{input_text}"')
            print("--- " * 15)
            for row in rows:
                if row[3] is None and row[4] is None:
                    salary = "Зарплата не указана"
                elif type(row[3]) is int and row[4] is None:
                    salary = f"Зарплата от {row[3]}"
                elif row[3] is None and type(row[4]) is int:
                    salary = f"Зарплата до {row[4]}"
                else:
                    salary = f"Зарплата от {row[3]} до {row[4]}"
                print(f"Компания: {row[1]} " f"Вакансия: {row[2]} " f"{salary} " f"URL: {row[5]} ")

            cur.close()
            self.conn.close()
