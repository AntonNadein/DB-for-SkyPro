from src.class_db_manager import DBCreate
from src.class_get_API import HeadHunterAPI


def selection_condition(
    question: str,
    answer_one: str,
    answer_two: str,
    answer_three: str = "",
    answer_four: str = "",
    answer_five: str = "",
) -> str:
    """
    Функция логики выбора
    :param question: Условие
    :param answer_one: Первый ответ
    :param answer_two: Второй ответ
    :param answer_three: Третий ответ
    :param answer_four: Четвертый ответ
    :param answer_five: Пятый ответ
    :return: Один из ответов
    """
    while True:
        string = (input(f"{question}:\n")).lower()
        if string in [answer_one.lower()]:
            return "1"
        elif string in [answer_two.lower()]:
            return "2"
        elif string in [answer_three.lower()]:
            return "3"
        elif string in [answer_four.lower()]:
            return "4"
        elif string in [answer_five.lower()]:
            return "5"
        elif string in ["0"]:
            return "exit"


def create_list(input_text):
    """Функция получения списка из стоки делитель:','"""
    if ", " in input_text:
        create_list = input_text.split(", ")
        return create_list
    elif "," in input_text:
        create_list = input_text.split(",")
        return create_list
    return input_text


def creation_filling_data_base(search_text, create_base):
    hh_api = HeadHunterAPI(search_text)
    get_vacancies = hh_api.get_vacancies_from_employer_id()
    create_base.data = get_vacancies
    create_base = DBCreate(get_vacancies)
    create_base.insert_table()
