from abc import ABC, abstractmethod


class AbstractDataProcessing(ABC):
    """
    Абстрактный класс для обработки данных о вакансиях, полученных с разных платформ.
    """

    @abstractmethod
    def add_vacancy(self, vacancy):
        """
        Абстрактный метод для добавления вакансий в файл.
        """
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, specified_criteria):
        """
        Абстрактный метод для получения данных из файла по указанным критериям.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """
        Абстрактный метод для удаления информации о вакансиях из файла.
        """
        pass
