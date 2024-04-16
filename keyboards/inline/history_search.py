from typing import Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.supporting_funcs import SupportFuncsInterface

get_user_history = SupportFuncsInterface.get_user_history()


def history_markup(db_request) -> Union[InlineKeyboardMarkup, str]:
    """
    Функция для создания экранной клавиатуры с историей запросов пользователя
    :param db_request: информация, полученная из базы данных
    :return: (InlineKeyboardMarkup) экранная клавиатура или сообщение об отсутствии истории запросов
    """
    user_history = get_user_history(db_request)
    if not isinstance(user_history, str):
        history_keyboard = InlineKeyboardMarkup()
        for i_row in user_history:
            history_keyboard.add(InlineKeyboardButton(text=i_row[0],
                                                      callback_data=i_row[1]))
        return history_keyboard
    else:
        return user_history
