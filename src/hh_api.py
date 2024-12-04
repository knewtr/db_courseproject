import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__url_emp = "https://api.hh.ru/employers"
        self.__url_vac = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {}


    def get_response(self) -> bool:
        """Метод подключения к API"""
        response = requests.get(self.__url_emp, headers=self.__headers, params=self.__params)
        status_code = response.status_code
        self.__params["page"] = 0
        if status_code == 200:
            return True
        else:
            return False

    def get_employers(self, employers_list: list[str]) -> list[dict]:
        """Метод для получения данных о работодателе"""
        employers = []
        if self.get_response():
            self.__url_emp = "https://api.hh.ru/employers"
            self.__params["sort_by"] = "by_name"
            self.__params["per_page"] = 100
        for employer in employers_list:
            self.__params['text'] = employer
            response = requests.get(self.__url_emp, headers=self.__headers, params=self.__params)
            data = response.json()
            employer_data = data['items'][0]
            id_ = employer_data.get('id')
            name = employer_data.get('name')
            url = employer_data.get('url')
            employers.append({'employer_id': id_, 'employer_name': name, 'company_url':url})
        return employers

    def get_vacancies(self, employer_id: str) -> list[dict]:
        """Метод для получения данных о вакансиях по id компании"""
        vacancies = []
        self.__params["employer_id"] = employer_id
        self.__params["per_page"] = 100
        if self.get_response():
            response = requests.get(self.__url_vac, headers=self.__headers, params=self.__params)
            data = response.json()
            items = data.get('items', [])
            vacancies.extend(items)
            return vacancies
