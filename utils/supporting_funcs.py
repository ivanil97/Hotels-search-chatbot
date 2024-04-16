from typing import Union
from peewee import ModelSelect
from telebot.types import CallbackQuery


def _get_city_name(call: CallbackQuery, city_id: str) -> str:
    """
    Функция для получения названия города из json-словаря, передающегося в функцию при нажатии пользователем
    определенной кнопки
    :param call: CallbackQuery от пользователя в чат-боте
    :param city_id: (str) id локации
    :return: название города или текст 'None'
    """
    city_list = call.json['message']['reply_markup']['inline_keyboard']
    for i_city in city_list:
        if i_city[0]['callback_data'] == city_id:
            return i_city[0]['text']
    return 'None'


def get_value(some_json: dict, keys: list, default_value='-') -> str:
    """
    Функция для поиска значения в словаре по серии ключей
    :param some_json: (dict) словарь, в котором ищем
    :param keys: (list) список ключей
    :param default_value: (str) значение, которое возвращает функция, если при прохождении списка ключей
    значение не было найдено
    :return: (str) искомое значение в словаре, дефолтное значение или текст 'None'
    """
    for i_key in keys:
        value = some_json.get(i_key, default_value)
        if isinstance(value, dict):
            first_key = keys.index(i_key)
            inner_value = get_value(value, keys[first_key + 1:])
            if inner_value:
                return inner_value
        if isinstance(value, dict) or isinstance(value, list):
            value = '-'
        return value
    return 'None'


def _get_detailed_info(json_response: dict) -> str:
    """
    Функция, которая получает информацию об отеле из json-словаря и формирует строку для отправки пользователю
    :param json_response: (dict) словарь с информацией об отеле
    :return: (str) строка для отправки пользователю
    """
    name = get_value(json_response, ['data', 'propertyInfo', 'summary', 'name'])
    tagline = get_value(json_response, ['data', 'propertyInfo', 'summary', 'tagline'])
    address = get_value(json_response, ['data', 'propertyInfo', 'summary', 'location', 'address', 'addressLine'])
    rating = get_value(json_response, ['data', 'propertyInfo', 'summary', 'overview', 'propertyRating', 'rating'])

    detailed_info = '{0}\n{1}\nАдрес: {2}\nРейтинг: {3}'.format(name, tagline, address, rating)
    return detailed_info


def _get_user_history(db_data: ModelSelect) -> Union[list[list[str, str]], str]:
    """
    Функция для получения информации из БД для создания InlineKeyboard c последними запросами
    :param db_data:
    :return: (Union[list[list[str, str]], str]) список последних запросов пользователя в формате
    [button_text, callback_data] для передачи в функцию history_markup либо сообщение об отсутствии истории поиска
    """
    user_history = list()
    for index, i_row in enumerate(db_data):
        date = i_row.created_at.strftime('%d %b	%Y')

        button_text = ('{date} - {req_type}; \n{request}\n'.format(
            date=date, req_type=i_row.request_type, request=i_row.request_body))
        callback_data = '{id};{created_at};1'.format(id=i_row.user_id, created_at=i_row.created_at)

        user_history.append([button_text, callback_data])

    if not user_history:
        user_history = 'История поиска отсутствует'

    return user_history


class SupportFuncsInterface:
    """
    Класс SupportFuncsInterface собирает функции для приведения данных в удобную для пользователя форму

    Методы
    -------
    Все методы возвращают функцию, как объект

    get_city_name() - возвращает функцию _get_city_name (функция для получения названия локации из CallbackQuery)

    get_detailed_info() - возвращает функцию _get_detailed_info (функция для получения данных из json
    для отправки пользователю информации об отеле)

    get_user_history() - возвращает функцию _get_user_history (функция для получения информации из БД
    для создания InlineKeyboard c последними запросами)

    """

    @staticmethod
    def get_city_name():
        return _get_city_name

    @staticmethod
    def get_detailed_info():
        return _get_detailed_info

    @staticmethod
    def get_user_history():
        return _get_user_history
