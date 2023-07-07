from src.api_work.abstract_api import AbstractAPI
import requests


class HeadHunterAPI(AbstractAPI):
    """
    Класс подключается к API сайта HeadHunter и получает вакансии.
    """
    url = "https://api.hh.ru/vacancies"

    def __init__(self, url, vacancies_count=50):
        """
        Инициализация класса HeadHunterAPI.
        """
        self._url = url
        self._vacancies_count = vacancies_count

    def get_vacancies(self, job_title):
        """
        Метод для поиска вакансий через HeadHunter API.
        """
        params = {
            "text": job_title,
            "per_page": self._vacancies_count,
            "only_with_salary": True
        }

        result = requests.get(url=self._url, params=params)
        result_json = result.json()

        return result_json.get("items", [])
