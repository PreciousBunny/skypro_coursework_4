from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, job_title):
        """
        Абстрактный метод для поиска вакансий с разных платформ.
        """
        pass
