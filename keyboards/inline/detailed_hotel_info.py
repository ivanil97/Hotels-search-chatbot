from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def hotels_detail_markup(cur_option, total_options) -> InlineKeyboardMarkup:
    """
    Функция для создания клавиатуры, позволяющей переключаться между вариантами в запросе пользователя
    :param cur_option: (int) номер текущего варианта
    :param total_options: (int) общее количество найденных отелей по данному запросу
    :return: (InlineKeyboardMarkup) экранная клавиатура с возможностью переключения между вариантами
    """
    markup = InlineKeyboardMarkup()
    # markup для первого варианта
    if cur_option == 1:
        markup.add(InlineKeyboardButton(text=f'{cur_option}/{total_options}', callback_data='None'),
                   InlineKeyboardButton(text='Вперёд -->', callback_data=str(cur_option + 1)))

    # markup для последнего варианта
    elif cur_option == total_options:
        markup.add(InlineKeyboardButton(text='<-- Назад', callback_data=str(cur_option - 1)),
                   InlineKeyboardButton(text=f'{cur_option}/{total_options}', callback_data='None'))

    # markup для остальных вариантов
    else:
        markup.add(InlineKeyboardButton(text='<-- Назад', callback_data=str(cur_option - 1)),
                   InlineKeyboardButton(text=f'{cur_option}/{total_options}', callback_data='None'),
                   InlineKeyboardButton(text='Вперёд -->', callback_data=str(cur_option + 1)))

    return markup
