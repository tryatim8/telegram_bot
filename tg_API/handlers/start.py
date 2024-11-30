from datetime import datetime

from peewee import IntegrityError

from database.common.models import History, User
from tg_API.core import bot


@bot.message_handler(commands=['start'])
def handle_start(message) -> None:
    """Хэндлер команды старт, приветствует пользователя."""
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    try:
        User.create(
            user_id=user_id,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
        ).save()
    except IntegrityError:
        bot.reply_to(message, 'Рады снова видеть вас, {0}!'.format(
            message.from_user.first_name,
        ))
    bot.reply_to(message, 'Добро пожаловать, {0}!'.format(
        message.from_user.first_name,
    ))
    History.create(
        search_time=datetime.now(),
        user=user_id,
        command_name='start',
    ).save()
    bot.send_message(
        message.chat.id,
        ' '.join(
            (
                'Вас приветствует чат-бот поиска товаров интернет-магазина',
                ' Amazon.\nЧат-бот позволяет искать товары по названию с',
                'сортировкой по цене а также в заданном ценовом диапазоне.',
                'Также сохраняет историю использованных команд\nДля получения',
                'списка команд отправьте /help',
            ),
        ),
    )
