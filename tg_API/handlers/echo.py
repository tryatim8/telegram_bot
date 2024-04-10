from tg_API.core import bot
from database.common.models import User, History


@bot.message_handler(func=lambda message: True)
def echo_and_info(message):
    bot.send_message(message.from_user.id, message.text)
    bot.reply_to(message, 'Для начала работы отправьте /start\n'
                          'Для получения списка команд отправьте /help')
