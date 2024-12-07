from src.hh_api import HeadHunterAPI
from src.db_manager import DBManager
from src.utils import create_db, save_data_to_db
from config.config import config



def main():
    """Основная функция проекта, которая взаимодействует с пользователем"""
    default_db_name = 'employers'
    default_companies_list = [
         "Альфа-Банк", "Т-Банк", "Самокат (ООО Умный ритейл)", "СОГАЗ", "ПАО Ростелеком",
        "Rusprofile", "Контур", "Нетология", "Сима-ленд", 'УГМК']

    params = {
    "host": "localhost",
    "user": "postgres",
    "password": 1234,
    "port": 5432
    }

    query = input(
        '''Введите через пробел название(я) компании(й), информацию о которой(ых) вы хотите получить, или пропустите этот шаг.\nВ этом случае будет выводиться информация о дефолтных компаниях.'''
    ).split()

    db_name_query = input('''Задайте своё имя для базы данных или пропустите этот шаг.\nПо умолчанию создастся БД "employers".''')

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
        vacancies_list = vacancies.extend(HeadHunterAPI().get_vacancies(employer['employer_id']))


    create_db(db_name, params)  # Создать таблицы в БД

    save_data_to_db( employers_data, vacancies, default_db_name, params)  # Заполнить БД данными из API

    print('Данные о выбранных компаниях и их вакансиях собраны')

if __name__ == '__main__':
    main()