from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Хендлер для обработки текстовых сообщений без указанного состояния
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    bot.reply_to(
        message, "Для работы с чат-ботом используйте команды или кнопки на экране. "
                 "Для получения справки используйте команду /help")
