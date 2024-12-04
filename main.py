from src.hh_api import HeadHunterAPI
from src.db_manager import DBManager
from src.utils import create_db, save_data_to_db
from config.config import config



def main():
    """Основная функция проекта, которая взаимодействует с пользователем"""
    companies_list = [
        "Яндекс",
        # "VK",
        # "Тинькофф",
        # "Ozon",
        # "Авито",
        # "МТС Диджитал",
        # "Lamoda",
        # "Контур",
        # "Холдинг Т1",
        # "ЛАНИТ",
    ]

    params = {
    "host": "localhost",
    "user": "postgres",
    "password": 1234,
    "port": 5432
    }
    vacancies = []
    check_response = HeadHunterAPI().get_response()
    print(check_response)
    employers_data = HeadHunterAPI().get_employers(companies_list)
    for employer in employers_data:
        vacancies_list = vacancies.extend(HeadHunterAPI().get_vacancies(employer['employer_id']))


    create_db("employers", params)  # Создать таблицы в БД

    save_data_to_db( employers_data, vacancies, "employers", params)  # Заполнить БД данными из API

if __name__ == '__main__':
    main()