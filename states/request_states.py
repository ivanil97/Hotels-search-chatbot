from telebot.handler_backends import State, StatesGroup


class UserRequestStateLow(StatesGroup):
    """
    Класс-наследник StatesGroup для хранения состояний при прохождении сценария в команде /low

    Атрибуты
    -------
    place: пользователь ввел команду /low
    quantity: пользователь определил точную локацию
    options: пользователь определил количество необходимых вариантов
    details: пользователю необходимо подтвердить запрос, если запрос подтвержден,
    пользователь может получить детальную информацию о вариантах отелей
    """

    place = State()
    quantity = State()
    options = State()
    details = State()


class UserRequestStateHigh(StatesGroup):
    """
    Класс-наследник StatesGroup для хранения состояний при прохождении сценария в команде /high

    Атрибуты
    -------
    place: пользователь ввел команду /high
    quantity: пользователь определил точную локацию
    options: пользователь определил количество необходимых вариантов
    details: пользователю необходимо подтвердить запрос, если запрос подтвержден,
    пользователь может получить детальную информацию о вариантах отелей
    """

    place = State()
    quantity = State()
    options = State()
    details = State()


class UserRequestStateCustom(StatesGroup):
    """
    Класс-наследник StatesGroup для хранения состояний при прохождении сценария в команде /custom

    Атрибуты
    -------
    place: пользователь ввел команду /custom
    range_min: пользователь определил точную локацию
    range_max: пользователь определил нижнюю границу ценового диапазона
    quantity: пользователь определил верхнюю границу ценового диапазона
    options: пользователь определил количество необходимых вариантов
    details: пользователю необходимо подтвердить запрос, если запрос подтвержден,
    пользователь может получить детальную информацию о вариантах отелей
    """

    place = State()
    range_min = State()
    range_max = State()
    quantity = State()
    options = State()
    details = State()


class UserRequestStateHistory(StatesGroup):
    """
    Класс-наследник StatesGroup для хранения состояний при прохождении сценария в команде /history

    Атрибуты
    -------
    history: пользователь ввел команду /history
    """

    history = State()
