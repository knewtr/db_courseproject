from src.hh_api import HeadHunterAPI
from src.utils import create_db, save_data_to_db
from config import config

def main():
    """Основная функция проекта, которая взаимодействует с пользователем"""
    companies_list = [
        'Яндекс',
        'VK',
        'Тинькофф',
        'Ozon',
        'Авито',
        'МТС Диджитал',
        'Lamoda',
        'Контур',
        'Холдинг Т1',
        'ЛАНИТ'
    ]
    params = config()

    data = HeadHunterAPI().get_employer_data(companies_list)  # Получить информацию о вакансиях

    create_db('employers', params) # Создать таблицы в БД

    # save_data = save_data_to_db(data, params)  # Заполнить БД данными из API
