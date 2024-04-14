from datetime import datetime
from peewee import IntegrityError

from tg_API.core import bot
from database.common.models import User, History


@bot.message_handler(commands=['start'])
def handle_start(message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    try:
        User.create(
            user_id=user_id,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name
        ).save()
        bot.reply_to(message, 'Добро пожаловать, {}!'.format(message.from_user.first_name))
    except IntegrityError:
        bot.reply_to(message, 'Рады снова видеть вас, {}!'.format(message.from_user.first_name))
    History.create(
        search_time=datetime.now(),
        user=user_id,
        command_name='start'
    ).save()
    bot.send_message(
        message.chat.id,
        'Вас приветствует чат-бот поиска товаров интернет-магазина Amazon.\nЧат-бот позволяет искать товары по названию'
        ' с сортировкой по цене а также в заданном ценовом диапазоне. Также сохраняет историю использованных команд\n'
        'Для получения списка команд отправьте /help'
    )
