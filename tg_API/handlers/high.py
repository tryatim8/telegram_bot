from datetime import datetime

from tg_API.core import bot
from database.common.models import User, History
from tg_API.states import UserState
# from site_API.core import site_api


@bot.message_handler(commands=['high'])
def handle_high(message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:  # Проверка, зарегистрирован ли пользователь
        bot.reply_to(message, 'Вы не зарегистрированы. Напишите /start')
        return
    bot.send_message(message.from_user.id, 'Введите название товара.')
    bot.set_state(message.from_user.id, UserState.high_prod_name)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_high'] = {'user_id': user_id}


@bot.message_handler(state=UserState.high_prod_name)
def handle_high_prod_name(message) -> None:
    product_name = message.text
    bot.send_message(message.from_user.id, 'Введите количество товаров')
    bot.set_state(message.from_user.id, UserState.high_result_size)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_high']['product_name'] = product_name


@bot.message_handler(state=UserState.high_result_size)
def handle_high_result_size(message) -> None:
    try:
        result_size = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, 'Некорректный ввод (нужно натуральное число).\n'
                                               'Введите количество товаров ещё раз')
        return
    with bot.retrieve_data(message.from_user.id) as data:
        product_name = data['new_high']['product_name']
    History.create(  # Записываем вызов команды в базу данных
        search_time=datetime.now(),
        user=message.from_user.id,
        command_name='high',
        product_name=product_name,
        result_size=result_size
    ).save()

    # TODO Написать код, обрабатывающий запрос поиска товаров в AmazonAPI.
    # amazon_search = site_api.search_products()
    # response = amazon_search(url, 'iphone', headers, params)
    result = 'Те самые товары с Амазон по команде /high'
    bot.send_message(message.from_user.id, result)
    bot.delete_state(message.from_user.id)  # Убираем состояние
