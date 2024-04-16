from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Хендлер для обработки команды /start
    :param message: (Message) сообщение пользователя в чат-боте
    :return: None
    """
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!"
                          f"\nС помощью этого бота можно найти отели в любом месте"
                          f"\nДля справки используй команду /help")
