from datetime import datetime
from typing import List

from tg_API.core import bot
from database.common.models import User, History


@bot.message_handler(commands=['history'])
def handle_history(message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:  # Проверка, зарегистрирован ли пользователь
        bot.reply_to(message, 'Вы не зарегистрированы. Напишите /start')
        return
    bot.send_message(message.from_user.id,
                     'История запросов:\na-название товара, b-количество товаров, c-диапазон цен')
    user_history: List[History] = User.get(User.user_id == message.from_user.id).commands_history
    result = []
    for i_ord, i_elem in enumerate(reversed(user_history)):
        result.append(str(i_elem))
        if i_ord == 9:
            break
    result_send = '\n'.join(reversed(result))
    bot.send_message(message.from_user.id, result_send)
    History.create(  # Записываем вызов команды в базу данных
        search_time=datetime.now(),
        user=message.from_user.id,
        command_name='history'
    ).save()
