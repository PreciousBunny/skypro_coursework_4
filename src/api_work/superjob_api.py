from src.api_work.abstract_api import AbstractAPI
import requests
import os


class SuperJobAPI(AbstractAPI):
    """
    Класс подключается к API сайта SuperJob и получает вакансии.
    """
    url = "https://api.superjob.ru/2.0"

    def __init__(self, url, vacancies_count=50):
        """
        Инициализация класса SuperJobAPI.
        """
        self._url = url
        self._vacancies_count = vacancies_count

    def get_vacancies(self, job_title):
        """
        Метод для поиска вакансий через SuperJob API.
        """
        url = f"{self._url}/vacancies/"
        headers = {
            "X-Api-App-Id": os.getenv("SUPERJOB_API_KEY")
        }
        params = {
            "keywords": [[1, job_title]],
            "count": self._vacancies_count,
            "no_agreement": True
        }

        result = requests.get(url, headers=headers, params=params)
        result_json = result.json()

        return result_json.get("objects", [])
