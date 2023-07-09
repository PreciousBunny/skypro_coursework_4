from typing import Union


class Vacancy:
    """
    Класс для получения информации о вакансии.
    """

    def __init__(self, title: str, ref: str, salary: int, date_published: int):
        """
        Инициализирует экземпляр класса Vacancy.
        """
        self.__title = title
        self.__ref = ref
        self.__salary = salary
        self.__date_published = date_published

    @property
    def salary(self) -> int:
        """
        Метод доступа к приватному атрибуту с геттером для зарплаты вакансии.
        """
        return self.__salary

    @salary.setter
    def salary(self, value: Union[int, float, str]) -> None:
        """
        Метод определяет зарплату вакансии.
        """
        self.__salary = int(float(value))

    @property
    def title(self) -> str:
        """
        Метод доступа к приватному атрибуту с геттером для названия вакансии.
        """
        return self.__title

    @property
    def ref(self) -> str:
        """
        Метод доступа к приватному атрибуту с геттером для ссылки на вакансию.
        """
        return self.__ref

    @property
    def date_published(self) -> int:
        """
        Метод доступа к приватному атрибуту с геттером для даты публикации вакансии.
        """
        return self.__date_published

    def __repr__(self) -> str:
        """
        Магический метод для отображения информации об объекте класса Vacancy в режиме отладки (для разработчиков).
        """
        return f"Vacancy{self.__title, self.__ref, self.__salary, self.__date_published}"

    def __str__(self) -> str:
        """
        Магический метод для отображения информации об объекте класса Vacancy для пользователей.
        """
        return f"Vacancy: {self.__title}\n" \
               f"Reference: {self.__ref}\n" \
               f"Salary: от {self.__salary} руб.\n" \
               f"Date published: {self.__date_published}\n"

    def __eq__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнивает, "равен" ли данный объект класса Vacancy по размеру заработной платы,
        с заработной платой другого объекта.
        """
        return self.__salary == other.salary

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнивает, является ли данный объект класса Vacancy "меньше"
        по размеру заработной платы, относительно заработной платой другого объекта.
        """
        return self.__salary < other.salary

    def __le__(self, other: "Vacancy") -> bool:
        """
        Магический метод сравнивает, является ли данный объект класса Vacancy "меньше или равен"
        по размеру заработной платы, относительно заработной платой другого объекта.
        """
        return self.__salary <= other.salary

    def validate_data(self) -> bool:
        """
        Метод проверяет, являются ли данные о вакансии валидными.
        """
        if not all([self.__title, self.__ref, self.__salary, self.__date_published]):
            return False
        return True
