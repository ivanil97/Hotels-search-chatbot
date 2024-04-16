from loader import bot
from states.request_states import UserRequestStateCustom
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from database.core import DBInterface
from utils.site_api_handler import SiteApiInterface
from utils.site_api_config import url, headers_post, payload_hotels, payload_details
from utils.supporting_funcs import SupportFuncsInterface
from keyboards.inline.city_search import city_markup
from keyboards.inline.confirmation_inline import confirmation_markup
from keyboards.inline.detailed_hotel_info import hotels_detail_markup
from keyboards.reply.confirmation import confirm_choice
from json import dumps

get_hotels = SiteApiInterface.get_hotels()
get_details = SiteApiInterface.get_details()

get_detailed_info = SupportFuncsInterface.get_detailed_info()
get_city_name = SupportFuncsInterface.get_city_name()

create_db_data = DBInterface.create_data()


@bot.message_handler(commands=['custom'])
def custom(message: Message) -> None:
    """
    Хендлер для обработки команды /custom
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    # устанавливаем состояние пользователя
    bot.set_state(message.from_user.id, UserRequestStateCustom.place, message.chat.id)

    # запрашиваем локацию
    bot.send_message(message.from_user.id, 'Где ищем?', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: '/' not in message.text, state=UserRequestStateCustom.place)
def check_city(message: Message) -> None:
    """
    Хендлер для уточнения локации у пользователя (в рамках команды /custom)
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    # делаем запрос локации и уточняем у пользователя место с помощью Inline keyboard
    keyboard = city_markup(message.text)
    if not isinstance(keyboard, str):
        bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, keyboard)
        custom(message)


@bot.callback_query_handler(func=lambda call: call.data not in ['None', 'history'] and ';' not in call.data,
                            state=UserRequestStateCustom.place)
def get_product(call: CallbackQuery) -> None:
    """
    Хендлер для сохранения названия локации и id по локации, указанной пользователем
    и запроса минимального диапазона цены
    :param call: CallbackQuery от пользователя в чат-боте
    :return: None
    """
    # если пользователь не нашел подходящий вариант, предлагаем ему создать новый запрос
    if call.data == 'new_request':
        bot.send_message(call.from_user.id, 'Создайте новый запрос /custom')

    else:
        # устанавливаем состояние пользователя
        bot.set_state(call.from_user.id, UserRequestStateCustom.range_min)

        # записываем id и название локации
        with bot.retrieve_data(call.from_user.id) as data:
            data['location_id'] = call.data
            data['location_name'] = get_city_name(call, call.data)

        # запрашиваем диапазон значений выборки
        bot.send_message(call.from_user.id, 'Укажите минимальную цену')


@bot.message_handler(state=UserRequestStateCustom.range_min)
def get_range_min(message: Message) -> None:
    """
    Хендлер для сохранения минимального диапазона цены и запроса максимального диапазона цены
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    # контроль ввода данных
    if message.text.isdigit() and int(message.text) > 0:

        # устанавливаем состояние пользователя
        bot.set_state(message.from_user.id, UserRequestStateCustom.range_max, message.chat.id)

        # записываем минимальную границу диапазона
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = message.text
        bot.send_message(message.from_user.id, 'Укажите максимальную цену')
    else:
        bot.send_message(message.from_user.id, 'Введите целое число больше 0')


@bot.message_handler(state=UserRequestStateCustom.range_max)
def get_range_max(message: Message) -> None:
    """
    Хендлер для сохранения максимального диапазона цены и запроса количества вариантов
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        min_range = int(data['min_price'])
        if message.text.isdigit() and int(message.text) > 0:
            # контроль ввода данных
            if int(message.text) > min_range:
                # устанавливаем состояние пользователя
                bot.set_state(message.from_user.id, UserRequestStateCustom.quantity, message.chat.id)

                # записываем максимальную границу диапазона
                data['max_price'] = message.text

                bot.send_message(message.from_user.id, 'Сколько вариантов подобрать?')
            else:
                bot.send_message(message.from_user.id, f'Введите целое число больше минимальной границы - {min_range}')
        else:
            bot.send_message(message.from_user.id, 'Введите целое число больше 0')


@bot.message_handler(state=UserRequestStateCustom.quantity)
def get_quantity(message: Message) -> None:
    """
    Хендлер для сохранения количества вариантов и для подтверждения запроса у пользователя (в рамках команды /custom)
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    # контроль ввода данных
    if message.text.isdigit() and int(message.text) > 0:

        # устанавливаем состояние пользователя
        bot.set_state(message.from_user.id, UserRequestStateCustom.options, message.chat.id)

        # записываем количество необходимых вариантов
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['quantity'] = message.text

            # отправляем пользователю полученную информацию для подтверждения
            text = f'Где ищем - {data["location_name"]}\nДиапазон цены: от {data["min_price"]}$ до' \
                   f' {data["max_price"]}$\nКоличество вариантов - {data["quantity"]}\n\nВсе верно?'
            bot.send_message(message.from_user.id, text, reply_markup=confirm_choice())

    else:
        bot.send_message(message.from_user.id, 'Введите целое число больше 0')


@bot.message_handler(state=UserRequestStateCustom.options)
def get_hotels_list(message: Message) -> None:
    """
    Хендлер для поиска отелей по id локации и количеству вариантов
    и сохранения запроса пользователя в БД (в рамках команды /custom)
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    # подтверждение данных для запроса
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, 'Ищу отели по вашему запросу', reply_markup=ReplyKeyboardRemove())

        # устанавливаем состояние пользователя
        bot.set_state(message.from_user.id, UserRequestStateCustom.details, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

            # делаем запрос отелей
            payload_hotels['filters']['price']['max'] = int(data['max_price'])
            payload_hotels['filters']['price']['min'] = int(data['min_price'])
            response = get_hotels(url=url, headers=headers_post, location_id=data['location_id'],
                                  payload=payload_hotels)

            if 'errors' in response:
                bot.send_message(message.from_user.id, 'В данном диапазоне нет вариантов отелей. Введите новый запрос')
                custom(message)

            elif not isinstance(response, str):
                properties: list = response['data']['propertySearch']['properties']
                adjusted_quantity = min(int(data['quantity']), len(properties))
                data['quantity'] = adjusted_quantity
                properties = properties[:adjusted_quantity]

                # сохраняем найденные отели
                data['hotels'] = dict()
                for index, i_property in enumerate(properties):
                    data['hotels'][index + 1] = i_property

                # сохраняем запрос в БД истории запросов
                short_request = '{}; кол-во: {}'.format(data['location_name'], data['quantity'])
                hotels_str = dumps(data['hotels'])
                create_db_data(user_name=message.from_user.username, user_id=message.from_user.id,
                               request_type='/custom', request_body=short_request, hotels=hotels_str)

                # отправляем пользователю информацию по отелям
                bot.send_message(message.from_user.id, 'Нашли предложения по вашему запросу',
                                 reply_markup=confirmation_markup())

            else:
                bot.send_message(message.from_user.id, response)
                custom(message)

    elif message.text.lower() == 'новый запрос':
        custom(message)

    else:
        bot.send_message(message.from_user.id, 'Для подтверждения или отмены запроса используйте кнопки')


@bot.callback_query_handler(func=lambda call: call.data != 'None', state=UserRequestStateCustom.details)
def get_hotel_details(call: CallbackQuery) -> None:
    """
    Хендлер для направления пользователю найденных вариантов по его запросу
    и переключения между ними (в рамках команды /custom)
    :param call: CallbackQuery от пользователя в чат-боте
    :return: None
    """
    # получаем данные по отелям, сохраненные на предыдущем этапе сценария
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        property_num = int(call.data)
        key_property_id = data['hotels'][property_num]['id']
        price_per_night = round(data['hotels'][property_num]['price']['lead']['amount'], 2)
        currency = data['hotels'][property_num]['price']['lead']['currencyInfo']['code']
        photo_url = data['hotels'][property_num]['propertyImage']['image']['url']

        # делаем запрос по нужному
        response = get_details(url=url, headers=headers_post, property_id=key_property_id, payload=payload_details)
        if not isinstance(response, str):

            # формируем текст сообщения для отправки пользователю
            detailed_info = get_detailed_info(response)
            detailed_info += '\nЦена за ночь: {0} {1}'.format(price_per_night, currency)

            # отправляем пользователю информацию по конкретному отелю
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_photo(call.from_user.id, photo=photo_url, caption=detailed_info,
                           reply_markup=hotels_detail_markup(cur_option=property_num,
                                                             total_options=len(data['hotels'])))
        else:
            bot.send_message(call.from_user.id, response)
