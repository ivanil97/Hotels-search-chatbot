from telebot import TeleBot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """
    Функция для создания списка команд чат-бота
    :param bot: используемый бот
    :return: None
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
