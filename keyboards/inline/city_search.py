from typing import Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.site_api_handler import SiteApiInterface
from utils.site_api_config import url, params, headers_get

get_city = SiteApiInterface.get_city()


def city_markup(key_city: str) -> Union[InlineKeyboardMarkup, str]:
    """
    Функция для создания экранной клавиатуры на основании локаций, найденных по названию, заданному пользователем
    :param key_city: (str) название, заданное пользователем
    :return: (InlineKeyboardMarkup) экранная клавиатура или сообщение об ошибке
    """
    cities = get_city(url=url, params=params, headers=headers_get, location=key_city)
    if not isinstance(cities, str):
        destinations_keyboard = InlineKeyboardMarkup()
        for city in cities:
            destinations_keyboard.add(InlineKeyboardButton(text=city['city_name'],
                                                           callback_data=city['city_id']))
        destinations_keyboard.add(InlineKeyboardButton(text='Нет подходящего варианта',
                                                       callback_data='new_request'))
        return destinations_keyboard
    else:
        return cities
