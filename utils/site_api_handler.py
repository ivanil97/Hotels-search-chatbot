from typing import Union, Optional, Callable
import requests
from loguru import logger

logger.add('logging.log', format='{time} | {level} | {message}', level='TRACE',
           rotation='10 MB', compression='zip', serialize=True)


@logger.catch
def _make_response(method: str, url: str, headers: dict, timeout: int,
                   params: Optional[dict] = None, json: Optional[dict] = None) -> Union[dict, str]:
    """
    Универсальная функция, которая направляет запрос к серверу
    :param method (str): HTTP-метод GET или POST
    :param url (str): URL-адрес запроса
    :param headers (Dict): словарь, содержащий ключ API и API-host
    :param timeout (int): количество секунд ожидания ответа от сервера
    :param params (Optional[Dict]): словарь, содержащий параметры для работы с методом GET - необязательный аргумент
    :param json (Optional[Dict]): словарь, содержащий параметры для работы с методом POST - необязательный аргумент
    :return (Union[Dict, str]): результат запроса к серверу либо сообщение об ошибке
    """

    error_text = 'Произошла ошибка, создайте новый запрос'

    try:
        response = requests.request(method, url, headers=headers, params=params, timeout=timeout, json=json)

        if response is not None:
            if response.status_code == requests.codes.ok:
                response = response.json()
                return response
            else:
                logger.warning('Response status code: {0}'.format(response.status_code))
        return error_text

    except BaseException as exc:
        logger.exception(exc)
        return error_text


def _city_search(url: str, headers: dict, params: dict, location: str, timeout: int = 10,
                 method: str = 'GET', func: Callable = _make_response) -> Union[list[dict], str]:
    """
    Функция, которая направляет GET-запрос к серверу для поиска локаций по названию, заданному пользователем
    :param url (str): URL-адрес запроса
    :param headers (Dict): словарь, содержащий ключ API и API-host
    :param params (Dict): словарь, содержащий параметры для работы с методом GET, в т.ч. location
    :param location (str): название локации, введенное пользователем
    :param timeout (int): количество секунд ожидания ответа от сервера
    :param method (str): HTTP-метод GET
    :param func (Callable): универсальная функция _make_response
    :return (Union[List[Dict], str]): список найденных локаций и их id, сообщение об отсутствии локаций
    либо сообщение об ошибке
    """

    url = '{0}/locations/v3/search'.format(url)
    params['q'] = location
    dest_type = ['CITY', 'NEIGHBORHOOD', 'MULTIREGION']

    response = func(method, url, headers=headers, params=params, timeout=timeout)

    if isinstance(response, dict):
        cities = list()
        for dest in response['sr']:
            if dest.get('type') in dest_type:
                destination = dest['regionNames'].get('fullName')
                city_id = dest['gaiaId']
                cities.append({'city_name': destination,
                               'city_id': city_id})
        if len(cities) == 0:
            return 'По данному названию у нас нет данных, попробуйте другое'
        return cities
    return response


def _get_hotels(url: str, headers: dict, location_id: str, payload: dict, timeout: int = 10,
                method: str = 'POST', func: Callable = _make_response) -> Union[dict, str]:
    """
    Функция, которая направляет POST-запрос к серверу для поиска отелей по id локации
    :param url (str): URL-адрес запроса
    :param headers (Dict): словарь, содержащий ключ API и API-host
    :param location_id (str): id локации
    :param payload (Dict): словарь, содержащий параметры для работы с методом POST, в т.ч. location_id
    :param timeout (int): количество секунд ожидания ответа от сервера
    :param method (str): HTTP-метод POST
    :param func (Callable): универсальная функция _make_response
    :return (Union[Dict, str]): список найденных отелей в заданной локации либо сообщение об ошибке
    """

    url = '{0}/properties/v2/list'.format(url)
    payload['destination']['regionId'] = location_id

    response = func(method, url, headers=headers, json=payload, timeout=timeout)

    return response


def _get_details(url: str, headers: dict, property_id: str, payload: dict, timeout: int = 10,
                 method: str = 'POST', func: Callable = _make_response) -> Union[dict, str]:
    """
    Функция, которая направляет POST-запрос к серверу для получения детальной информации об отеле
    :param url (str): URL-адрес запроса
    :param headers (Dict): словарь, содержащий ключ API и API-host
    :param property_id (str): id отеля:
    :param payload (Dict): словарь, содержащий параметры для работы с методом POST, в т.ч. property_id
    :param timeout (int): количество секунд ожидания ответа от сервера
    :param method (str): HTTP-метод POST
    :param func (Callable): универсальная функция _make_response
    :return (Union[Dict, str]): детальная информация об отеле либо сообщение об ошибке
    """
    url = '{0}/properties/v2/detail'.format(url)
    payload['propertyId'] = property_id

    response = func(method, url, headers=headers, json=payload, timeout=timeout)

    return response


class SiteApiInterface:
    """
    Класс SiteApiInterface собирает функции для отправки запросов к API

    Методы
    -------
    Все методы возвращают функцию, как объект

    get_city() - возвращает функцию _city_search (GET-запрос к API для получения локаций по названию)

    get_hotels() - возвращает функцию _get_hotels (POST-запрос к API для получения отелей по id локации)

    get_details() - возвращает функцию _get_details (POST-запрос к API для получения детальной информации об отеле)

    """

    @staticmethod
    def get_city():
        return _city_search

    @staticmethod
    def get_hotels():
        return _get_hotels

    @staticmethod
    def get_details():
        return _get_details
