from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def history_detail_markup(call_data: str, total_options: int) -> InlineKeyboardMarkup:
    """
    Функция для создания клавиатуры, позволяющей переключаться между вариантами
    в запросе пользователя (в рамках команды /history)
    :param call_data: (str) информация, передающаяся в функцию при нажатии пользователем определенной кнопки
    :param total_options: (int) общее количество найденных отелей по данному запросу
    :return: (InlineKeyboardMarkup) экранная клавиатура с возможностью переключения между вариантами
    """
    markup = InlineKeyboardMarkup()
    user_id = call_data.split(';')[0]
    created_at = call_data.split(';')[1]
    cur_option = int(call_data.split(';')[2])

    # markup для первого варианта
    if cur_option == 1:
        next_option = cur_option + 1
        callback_data = f'{user_id};{created_at};{next_option}'
        markup.add(InlineKeyboardButton(text=f'{cur_option}/{total_options}', callback_data='None'),
                   InlineKeyboardButton(text='Вперёд -->', callback_data=callback_data),
                   InlineKeyboardButton(text='Вернуться к истории запросов', callback_data='history'))

    # markup для последнего варианта
    elif cur_option == total_options:
        prev_option = cur_option - 1
        callback_data = f'{user_id};{created_at};{prev_option}'
        markup.add(InlineKeyboardButton(text='<-- Назад', callback_data=callback_data),
                   InlineKeyboardButton(text=f'{cur_option}/{total_options}', callback_data='None'),
                   InlineKeyboardButton(text='Вернуться к истории запросов', callback_data='history'))

    # markup для остальных вариантов
    else:
        prev_option = cur_option - 1
        next_option = cur_option + 1
        prev_callback_data = f'{user_id};{created_at};{prev_option}'
        next_callback_data = f'{user_id};{created_at};{next_option}'
        markup.add(InlineKeyboardButton(text='<-- Назад', callback_data=prev_callback_data),
                   InlineKeyboardButton(text=f'{cur_option}/{total_options}', callback_data='None'),
                   InlineKeyboardButton(text='Вперёд -->', callback_data=next_callback_data),
                   InlineKeyboardButton(text='Вернуться к истории запросов', callback_data='history'))

    return markup
