from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def confirm_choice() -> ReplyKeyboardMarkup:
    """
    Функция для создания клавиатуры, позволяющей подтвердить запрос или создать новый
    :return: (ReplyKeyboardMarkup) экранная клавиатура
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Новый запрос'))
    return keyboard
