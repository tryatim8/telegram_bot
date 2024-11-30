from tg_API.core import bot


@bot.message_handler(func=lambda message: True)
def echo_and_info(message):
    bot.reply_to(message, 'Для начала работы отправьте /start\n'
                          'Для получения списка команд отправьте /help')
