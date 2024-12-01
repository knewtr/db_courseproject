import requests

class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""
    def __init__(self):
        self.url = "https://api.hh.ru/"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {}
        self.employers = []


    def get_response(self) -> bool:
        """Метод подключения к API"""
        response = requests.get("https://api.hh.ru/", headers=self.headers, params=self.params)
        status_code = response.status_code
        self.params["page"] = 0
        if status_code == 200:
            print("Ответ от hh.ru получен.")
            return True
        else:
            print(f"Ошибка подключения к hh.ru.")
            return False

    def get_employer_data(self, companies_list: list[str]) -> list[dict]:
        """Метод для получения данных о работодателе"""
        companies_list = []
        if self.get_response():
            self.url = "https://api.hh.ru/employers"
            self.params["sort_by"] = "by_name"
            self.params["per_page"] = 100
            while requests.get(self.url, headers=self.headers, params=self.params):
                response = requests.get(self.url, headers=self.headers, params=self.params)
                companies_list.extend(response.json()["items"])
        return companies_list


    def get_vacancies(self, employer_id: str) -> list[dict]:
        """Метод для получения данных о вакансиях по id компании"""
        vacancies = []
        if self.get_response():
            self.url = "https://api.hh.ru/vacancies"
            self.params["employer_id"] = "employer_id"
            self.params["per_page"] = 10
            while requests.get(self.url, headers=self.headers, params=self.params):
                response = requests.get(self.url, headers=self.headers, params=self.params)
                vacancies.extend(response.json()["items"])
                self.params["page"] += 1
        return vacancies
