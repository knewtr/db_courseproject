import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {}


    def _get_response(self) -> bool:
        """Метод подключения к API"""
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        status_code = response.status_code
        if status_code == 200:
            return True
        else:
            return False

    def get_employers(self, employers_list: list[str]) -> list[dict]:
        """Метод для получения данных о работодателе"""
        employers = []
        if self._get_response():
            self.__url = "https://api.hh.ru/employers"
            self.__params["sort_by"] = "by_vacancies_open"
            self.__params["per_page"] = 10
        for employer in employers_list:
            self.__params['text'] = employer
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            data = response.json()
            print(data)
            if data.get('items'):
                for employer_data in data['items']:
                    if employer_data.get('name') == employer:
                        id_ = employer_data.get('id')
                        name = employer_data.get('name')
                        url = employer_data.get('alternate_url')
                        employers.append({'employer_id': id_, 'employer_name': name, 'company_url': url})
            else:
                employers.append({'employer_name': employer, 'error': 'Данные отсутствуют'})
        return employers

    def get_vacancies(self, employer_id: str) -> list[dict]:
        """Метод для получения данных о вакансиях по id компании"""
        vacancies = []
        self.__params["employer_id"] = employer_id
        self.__params["per_page"] = 10
        if self._get_response():
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            data = response.json().get('items', [])
            print(data)
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies


# if __name__ == '__main__':
#     companies_list = [
#          "Альфа-Банк", "Т-Банк", "Самокат (ООО Умный ритейл)", "СОГАЗ", "ПАО Ростелеком",
#         "Rusprofile", "Контур", "Нетология", "Сима-ленд", 'УГМК']
#
#     params = {
#         "host": "localhost",
#         "user": "postgres",
#         "password": 1234,
#         "port": 5432
#     }
#
#     vacancies = []
#     check_response = HeadHunterAPI()._get_response()
#     print(check_response)
#     employers_data = HeadHunterAPI().get_employers(companies_list)
#     print(employers_data)
#     for employer in employers_data:
#         vacancies_data = vacancies.extend(HeadHunterAPI().get_vacancies(employer['employer_id']))
