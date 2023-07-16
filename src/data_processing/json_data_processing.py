from src.data_processing.abstract_data_processing import AbstractDataProcessing
from src.vacancy import Vacancy
import json


class JSONDataProcessing(AbstractDataProcessing):
    """
    Класс для обработки данных о вакансиях, полученных с разных платформ и сохраненных в JSON файле.
    """

    def __init__(self, path):
        """
        Инициализирует экземпляр класса JSONDataProcessing.
        """
        self.path = path

    def add_vacancy(self, vacancy: Vacancy):
        """
        Метод для добавления вакансий в JSON файл.
        """
        with open(self.path, "a", encoding="utf-8") as file:
            vacancy_dict = {
                "title": vacancy.title,
                "Link": vacancy.link,
                "salary": vacancy.salary,
                "Date published": vacancy.date_published
            }
            json.dump(vacancy_dict, file, ensure_ascii=False)
            file.write("\n")

    def get_vacancies_by_criteria(self, specified_criteria):
        """
        Метод для получения данных (списка вакансий) из JSON файла по указанным критериям.
        """
        vacancies = []
        with open(self.path, "r", encoding="utf-8") as file:
            for line in file:
                vacancy_data = json.loads(line)
                if self.vacancy_relevant_criteria(vacancy_data, specified_criteria):
                    vacancies.append(vacancy_data)
        return vacancies

    def delete_vacancy(self, vacancy: Vacancy):
        """
        Метод для удаления информации о вакансиях из JSON файла.
        """
        with open(self.path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open(self.path, "w", encoding="utf-8") as file:
            for line in lines:
                vacancy_data = json.loads(line)
                if not self.equality_of_vacancies(vacancy_data, vacancy):
                    file.write(line)

    @staticmethod
    def vacancy_relevant_criteria(vacancy_data, specified_criteria):
        """
        Метод проверяет, соответствует ли вакансия указанным критериям.
        """
        for key, value in specified_criteria.items():
            if key not in vacancy_data or vacancy_data[key] != value:
                return False
        return True

    @staticmethod
    def equality_of_vacancies(vacancy_data1, vacancy_data2):
        """
        Метод проверяет, равны ли две вакансии.
        """
        return vacancy_data1 == vacancy_data2
