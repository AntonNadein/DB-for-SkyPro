from src.class_db_manager import DBCreate, DBManager
from src.class_get_API import HeadHunterAPI
from src.utils import create_list, selection_condition, creation_filling_data_base


# дописать взаимодействие с пользователем и тесты

def main():
    create_base = DBCreate('None')
    print(create_base.data)
    create_base.create_table()
    text_input = input("Вветите компанию для поиска, или список компаний через запятую\n"
                       "Пример: Газпром или Газпром, Сбербанк, Ростелеком\n"
                       ": ")
    text_input = create_list(text_input)
    if type(text_input) is str:
        creation_filling_data_base(text_input, create_base)
    else:
        for item_list in text_input:
            creation_filling_data_base(item_list, create_base)

    manage_base = DBManager()
    while True:
        print("--- " * 10)
        text = ("Сортировка базы данных, введите цифру номер пункта сортировки\n"
                "1 - Выводит список всех компаний и количество вакансий у каждой компании\n"
                "2 - Выводит список всех вакансий с указанием названия компании, названия вакансии "
                "и зарплаты и ссылки на вакансию\n"
                "3 - Выводит среднюю зарплату по вакансиям\n"
                "4 - Выводитсписок всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                "5 - Выводит список всех вакансий, в названии которых содержатся искомое слово\n"
                "0 - Для выхода из программы")
        answer = selection_condition(text, "1", "2", "3","4","5")
        if answer == "1":
            manage_base.get_companies_and_vacancies_count()
        elif answer == "2":
            manage_base.get_all_vacancies()
        elif answer == "3":
            manage_base.get_avg_salary()
        elif answer == "4":
            manage_base.get_vacancies_with_higher_salary()
        elif answer == "5":
            text_2 = input("Введите текст для поиска\n"
                              "Внимание поиск регистрозависим т.е.\n"
                              "'Аналитик' и 'аналитик' это разные слова\n"
                              ": ")
            manage_base.get_vacancies_with_keyword(text_2)
        elif answer == "exit":
            break


if __name__ == '__main__':
    main()
