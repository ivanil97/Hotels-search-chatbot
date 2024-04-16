from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirmation_markup() -> InlineKeyboardMarkup:
    """
    Функция для создания экранной клавиатуры, отправляющей пользователю найденные варианты отелей
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Показать предложения', callback_data='1'))
    return markup
