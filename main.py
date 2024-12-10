from config.config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.utils import create_db, save_data_to_db


def main():
    """Основная функция проекта, которая взаимодействует с пользователем"""
    default_db_name = "employers"
    default_companies_list = [
        "Альфа-Банк",
        "Т-Банк",
        "Самокат (ООО Умный ритейл)",
        "СОГАЗ",
        "ПАО Ростелеком",
        "Rusprofile",
        "Контур",
        "Нетология",
        "РМК",
        "УГМК",
    ]

    params = config()

    query = input(
        """Введите через пробел название(я) компании(й), информацию о которой(ых) вы хотите получить, или пропустите этот шаг.\nВ этом случае будет выводиться информация о дефолтных компаниях."""
    ).split()

    db_name_query = input(
        """Задайте своё имя для базы данных или пропустите этот шаг.\nПо умолчанию создастся БД "employers"."""
    )

    vacancies = []

    if db_name_query:
        db_name = db_name_query
    else:
        db_name = default_db_name

    if query:
        query_companies_list = query
    else:
        query_companies_list = default_companies_list

    # check_response = HeadHunterAPI()._get_response()
    # print(check_response)

    employers_data = HeadHunterAPI().get_employers(query_companies_list)
    for employer in employers_data:
        vacancies.extend(HeadHunterAPI().get_vacancies(employer["employer_id"]))
    vacancies_list = list(map(lambda x: HeadHunterAPI.change_data(x), vacancies))
    # print(f'Полученные вакансии: {vacancies_list}')

    create_db(db_name, params)  # Создать таблицы в БД

    save_data_to_db(
        employers_data, vacancies_list, default_db_name, params
    )  # Заполнить БД данными из API

    DBManager(db_name, params).get_companies_and_vacancies_count()

    options_query = input(
        """Данные о выбранных компаниях и их вакансиях собраны. Выберите одну из опций:
        1 - Вывести все вакансии;
        2 - Вывести среднюю зарплату по вакансиям;
        3 - Вывести вакансии с заработной платой выше среднего;
        4 - Вывести вакансии по ключевому слову;
        5 - Завершить работу;\n
        """
    )
    while True:
        if options_query == "1":
            rows = DBManager(db_name, params).get_all_vacancies()
            for row in rows:
                print(
                    f"Название компании: {row[0]}.\nНазвание вакансии: {row[1]}.\nЗаработная плата: {row[2]} руб.\nСсылка на вакансию: {row[3]}"
                )
        elif options_query == "2":
            result = DBManager(db_name, params).get_avg_salary()
            print(f"Средняя зарплата для всех вакансий: {result} руб.")
        elif options_query == "3":
            rows = DBManager(db_name, params).get_vacancies_with_higher_salary()
            for row in rows:
                print(
                    f"Название вакансии: {row[2]}.\nЗаработная плата: {row[3]} руб.\nСсылка на вакансию: {row[4]}"
                )
        elif options_query == "4":
            key_word = input("Введите ключевое слово.\n")
            rows = DBManager(db_name, params).get_vacancies_with_keyword(key_word)
            for row in rows:
                print(
                    f"Название вакансии: {row[2]}.\nЗаработная плата: {row[3]} руб.\nСсылка на вакансию: {row[4]}"
                )
        elif options_query == "5":
            print("Работа завершена.")
            break
        else:
            options_query = input(
                "Введен неверный номер операции. Выберите одну из опций от 1 до 5.\n"
            )

# if __name__ == '__main__':
#     main()