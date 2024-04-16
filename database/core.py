from peewee import ModelSelect
from database.model import db, RequestHistory

db.connect()
db.create_tables([RequestHistory])


def _store_data(user_id: str, user_name: str, request_type: str, request_body: str, hotels: dict,
                table_class=RequestHistory) -> None:
    """
    Функция для создания записи в БД
    :param user_id: (str) id пользователя
    :param user_name: никнейм пользователя
    :param request_type: (str) название функции, которую вызвал пользователь (low, high, custom)
    :param request_body: (str) краткое описание запроса
    :param hotels: (dict) словарь с данными по отелям, найденным в рамках запроса
    :param table_class: (RequestHistory) используемая БД
    :return: None
    """
    with db:
        table_class.create(user_id=user_id, user_name=user_name, request_type=request_type,
                           request_body=request_body, hotels=hotels)


def _retrieve_data(user_id: str, table_class=RequestHistory) -> ModelSelect:
    """
    Функция для получения информации по всем запросам пользователя на основании его id
    :param user_id: (str) id пользователя
    :param table_class: (RequestHistory) используемая БД
    :return: (ModelSelect) записи из БД по заданному критерию
    """
    with db:
        response = table_class.select().where(table_class.user_id == user_id)

        return response


def _retrieve_hotels(user_id: str, request_date: str, table_class=RequestHistory) -> ModelSelect:
    """
    Функция для получения информации по отелям, найденным по конкретному запросу
    :param user_id: (str) id пользователя
    :param request_date: (str) время и дата создания запроса
    :param table_class: (RequestHistory) используемая БД
    :return: (ModelSelect) записи из БД по заданному критерию
    """
    with db:
        response = table_class.select().where(table_class.user_id == user_id
                                              and table_class.created_at == request_date)

        return response


class DBInterface:
    """Класс DBInterface собирает функции для работы с БД

    Methods
    -------
    Все методы возвращают функцию, как объект

    create_data() - возвращает функцию _store_data (создание строки в БД)

    retrieve_data() - возвращает функцию _retrieve_data (получение строк БД по определенному id пользователя)

    retrieve_hotels() - возвращает функцию _retrieve_hotels (получение данных по выбранному пользователем запросу
    из истории поиска)

    """

    @staticmethod
    def create_data():
        return _store_data

    @staticmethod
    def retrieve_data():
        return _retrieve_data

    @staticmethod
    def retrieve_hotels():
        return _retrieve_hotels
