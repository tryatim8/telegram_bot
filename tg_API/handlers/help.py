from datetime import datetime

from tg_API.core import bot
from database.common.models import User, History
from config import DEFAULT_COMMANDS


@bot.message_handler(commands=['help'])
def handle_help(message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:  # Проверка, зарегистрирован ли пользователь
        bot.reply_to(message, 'Вы не зарегистрированы. Напишите /start')
        return
    # Скрепляем кортеж кортежей в единую строку
    commands_str = '\n'.join(['/{0} - {1}'.format(i_comm[0], i_comm[1])
                              for i_comm in DEFAULT_COMMANDS])
    bot.send_message(message.chat.id, 'Список команд:\n{}'.format(commands_str))
    History.create(
        search_time=datetime.now(),
        user=message.from_user.id,
        command_name='help'
    ).save()
