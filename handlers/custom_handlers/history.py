from keyboards.inline.detailed_history_info import history_detail_markup
from loader import bot
from states.request_states import UserRequestStateHistory
from database.core import DBInterface
from telebot.types import Message, CallbackQuery
from utils.supporting_funcs import SupportFuncsInterface
from keyboards.inline.history_search import history_markup
from utils.site_api_handler import SiteApiInterface
from utils.site_api_config import url, headers_post, payload_details
from json import loads


get_db_data = DBInterface.retrieve_data()
get_db_hotels = DBInterface.retrieve_hotels()

get_details = SiteApiInterface.get_details()
get_detailed_info = SupportFuncsInterface.get_detailed_info()


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """
    Хендлер для обработки команды /history
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    # устанавливаем состояние пользователя
    bot.set_state(message.from_user.id, UserRequestStateHistory.history, message.chat.id)

    # Получаем из БД список запросов и оставляем 10 последних строк
    db_request = get_db_data(message.from_user.id)

    start_row = 0
    if len(db_request) > 10:
        start_row = len(db_request) - 10
    db_request = db_request[start_row:]

    # Собираем данные, полученные из БД, для отправки пользователю
    user_history_keyboard = history_markup(db_request)

    if not isinstance(user_history_keyboard, str):
        # Отправляем данные пользователю
        bot.send_message(message.from_user.id, 'Вот ваша история запросов:', reply_markup=user_history_keyboard)
    else:
        bot.send_message(message.from_user.id, user_history_keyboard)


@bot.callback_query_handler(func=lambda call: call.data != 'None', state=UserRequestStateHistory.history)
def get_hotel_details(call: CallbackQuery) -> None:
    """
    Хендлер для отправки пользователю запросов из истории его запросов и переключения между найденными отелями
    :param call: CallbackQuery от пользователя в чат-боте
    :return: None
    """
    if call.data == 'history':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.from_user.id, 'Введите команду /history')
    else:
        # получаем данные по отелям из БД
        user_id = call.data.split(';')[0]
        request_date = call.data.split(';')[1]
        property_num = call.data.split(';')[2]

        db_request = get_db_hotels(user_id, request_date)

        hotels = dict()
        for i_row in db_request:
            hotels = i_row.hotels
        hotels = loads(hotels)

        if hotels:
            key_property_id = hotels[property_num]['id']
            price_per_night = round(hotels[property_num]['price']['lead']['amount'], 2)
            currency = hotels[property_num]['price']['lead']['currencyInfo']['code']
            photo_url = hotels[property_num]['propertyImage']['image']['url']

            # делаем запрос по нужному отелю
            response = get_details(url=url, headers=headers_post, property_id=key_property_id, payload=payload_details)

            if not isinstance(response, str):
                # формируем текст сообщения для отправки пользователю
                detailed_info = get_detailed_info(response)
                detailed_info += '\nЦена за ночь: {0} {1}'.format(price_per_night, currency)

                # отправляем пользователю информацию по конкретному отелю
                bot.delete_message(call.message.chat.id, call.message.id)
                call_data = f'{user_id};{request_date};{property_num}'
                bot.send_photo(call.from_user.id, photo=photo_url, caption=detailed_info,
                               reply_markup=history_detail_markup(call_data=call_data, total_options=len(hotels)))
            else:
                bot.send_message(call.from_user.id, response)
        else:
            bot.send_message(call.from_user.id, 'Отели в данной локации не были найдены')
