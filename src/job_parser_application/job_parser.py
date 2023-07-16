from src.api_work.hh_api import HeadHunterAPI
from src.api_work.superjob_api import SuperJobAPI
from src.data_processing.json_data_processing import JSONDataProcessing
from src.vacancy import Vacancy
from src.job_parser_application.job_parser_application_meta import JobParserApplicationMeta

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class JobParser(metaclass=JobParserApplicationMeta):
    """
    Класс "создает" приложение по поиску вакансий.
    """
    _vacancies = []
    _hh_api = HeadHunterAPI()
    _superjob_api = SuperJobAPI()
    _json_data_processing = JSONDataProcessing("json_found_vacancies.json")
    _job_title = None
    _top_vacancy = None

    @classmethod
    def _user_interaction(cls):
        """
        Метод для взаимодействия с пользователем.
        """
        print("\nВас приветствует приложение по поиску работы. Давайте начнем:")

        while True:
            print("\n1. Поиск вакансий на платформах \"HeadHunter\", \"SuperJob\"")
            print("2. Вывести найденные вакансии на экран")
            print("3. Сохранить найденные вакансии в файл")
            print("0. Выход (exit)")
            menu_command_selection = input("\nПожалуйста, выберите один из предложенных вариантов:\n>_ ")

            if menu_command_selection == "1":
                cls._job_title = input("Введите желаемую должность для поиска:\n>_ ")
                cls._search_vacancies()
                cls._top_vacancy = int(input("Введите количество вакансий для вывода в ТОП-листе:\n>_ "))
                while True:
                    print("\n1. Сортировка по дате публикации вакансии")
                    print("2. Сортировка по окладу вакансии\n")
                    sort_selection = input("Выберите вариант сортировки:\n>_ ")
                    if sort_selection == "1":
                        cls._sorted_vacancy_by_date_published()
                        break
                    elif sort_selection == "2":
                        cls._sorted_vacancy_by_salary()
                        break
                    else:
                        print("Некорректный выбор варианта сортировки. Попробуйте выбрать еще раз!")
            elif menu_command_selection == "2":
                cls._vacancies_display_output()
            elif menu_command_selection == "3":
                if cls._vacancies:
                    cls._save_vacancies_to_file()
                    print("Вакансии были сохранены в файл.")
                else:
                    print("Нет доступных вакансий для сохранения. Попробуйте изменить условия поиска!")
            elif menu_command_selection == "0":
                print("Спасибо, что воспользовались нашим приложением! Мы рады были Вам помочь!\n")
                break
            else:
                print("Некорректный выбор варианта. Попробуйте выбрать еще раз! (подсказка - введите число от 0 до 3)")

    @classmethod
    def _search_vacancies(cls) -> None:
        """
        Метод для поиска вакансий на платформах "HeadHunter", "SuperJob".
        """
        with ThreadPoolExecutor() as executor:
            hh_future = executor.submit(cls._hh_api.get_vacancies, cls._job_title)
            superjob_future = executor.submit(cls._superjob_api.get_vacancies, cls._job_title)
            hh_vacancies = hh_future.result()
            superjob_vacancies = superjob_future.result()
            for vacancy_data in hh_vacancies + superjob_vacancies:
                title = cls._get_title(vacancy_data)
                link = cls._get_link(vacancy_data)
                salary_from = cls._get_salary(vacancy_data)
                date_published = cls._get_date_published(vacancy_data)
                currency = cls._get_currency(vacancy_data)
                cls._check_currency_and_adding(title, link, salary_from, date_published, currency)

        return cls._filtered_vacancies_by_title()

    @staticmethod
    def _get_title(vacancy) -> str:
        """
        Метод для получения названия вакансии.
        """
        return vacancy["profession"] if vacancy.get("profession") is not None else vacancy["name"]

    @staticmethod
    def _get_link(vacancy) -> str:
        """
        Метод для получения ссылки на вакансию.
        """
        return vacancy["link"] if vacancy.get("link") is not None else vacancy["alternate_url"]

    @staticmethod
    def _get_salary(vacancy) -> int:
        """
        Метод для получения оклада по вакансии.
        """
        return vacancy["payment_from"] if vacancy.get("payment_from") is not None else vacancy["salary"]["from"]

    @staticmethod
    def _get_date_published(vacancy) -> str:
        """
        Метод для получения даты публикации вакансии.
        """
        return datetime.utcfromtimestamp(vacancy["date_published"]).strftime('%Y.%m.%d') if vacancy.get(
            "date_published") is not None else datetime.fromisoformat(vacancy["published_at"]).strftime("%Y.%m.%d")

    @staticmethod
    def _get_currency(vacancy) -> str:
        """
        Метод для получения валюты оклада по вакансии.
        """
        return vacancy["currency"].upper() if vacancy.get("currency") else vacancy["salary"]["currency"].upper()

    @classmethod
    def _check_currency_and_adding(cls, title, link, salary, date_published, currency) -> None:
        """
        Метод проверяет валюту, и добавляет вакансии в список вакансий.
        """
        if currency in ["RUR", "RUB"] and salary:
            cls._vacancies.append(Vacancy(title, link, salary, date_published))

    @classmethod
    def _filtered_vacancies_by_title(cls) -> None:
        """
        Метод для фильтрации вакансий по их названию.
        """
        cls._vacancies = list(filter(lambda x: cls._job_title.lower() in x.title.lower() and x.salary is not None,
                                     cls._vacancies))

    @classmethod
    def _sorted_vacancy_by_salary(cls) -> None:
        """
        Метод сортировки вакансий по их окладу.
        """
        if cls._top_vacancy > len(cls._vacancies):
            print(f"Всего было найдено вакансий: {len(cls._vacancies)}")
        cls._vacancies = sorted(cls._vacancies, key=lambda x: x.salary, reverse=True)[
                         :cls._top_vacancy]

    @classmethod
    def _sorted_vacancy_by_date_published(cls) -> None:
        """
        Метод сортировки вакансий по их дате публикации.
        """
        if cls._top_vacancy > len(cls._vacancies):
            print(f"Всего было найдено вакансий: {len(cls._vacancies)}")
        cls._vacancies = sorted(cls._vacancies, key=lambda x: x.date_published, reverse=True)[
                         :cls._top_vacancy]

    @classmethod
    def _vacancies_display_output(cls) -> None:
        """
        Метод для вывода найденных вакансий на дисплей.
        """
        if cls._vacancies:
            print("Вакансии:")
            [print(vacancy) for vacancy in cls._vacancies]
        else:
            print("Нет доступных вакансий для вывода на экран. Попробуйте изменить условия поиска!")

    @classmethod
    def _save_vacancies_to_file(cls) -> None:
        """
        Метод для сохранения найденных вакансий в JSON файл.
        """
        for vacancy in cls._vacancies:
            cls._json_data_processing.add_vacancy(vacancy)
