from datetime import datetime

from tg_API.core import bot
from database.common.models import User, History
from tg_API.states import UserState
# from site_API.core import site_api


@bot.message_handler(commands=['custom'])
def handle_custom(message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:  # Проверка, зарегистрирован ли пользователь
        bot.reply_to(message, 'Вы не зарегистрированы. Напишите /start')
        return
    bot.send_message(message.from_user.id, 'Введите название товара.')
    bot.set_state(message.from_user.id, UserState.custom_prod_name)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_custom'] = {'user_id': user_id}


@bot.message_handler(state=UserState.custom_prod_name)
def handle_custom_prod_name(message) -> None:
    product_name = message.text
    bot.send_message(message.from_user.id, 'Введите количество товаров')
    bot.set_state(message.from_user.id, UserState.custom_result_size)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_custom']['product_name'] = product_name


@bot.message_handler(state=UserState.custom_result_size)
def handle_custom_result_size(message) -> None:
    try:
        result_size = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, 'Некорректный ввод (нужно натуральное число).\n'
                                               'Введите количество товаров ещё раз')
        return
    bot.send_message(message.from_user.id, 'Введите диапазон цен через пробел')
    bot.set_state(message.from_user.id, UserState.custom_result_size)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_custom']['result_size'] = result_size


@bot.message_handler(state=UserState.custom_price_range)
def handle_custom_price_range(message) -> None:
    price_range_str = message.text
    try:
        price_range_list = list(map(int, price_range_str.split(' ')[:2]))
    except (ValueError, IndexError):
        bot.send_message(message.from_user.id, 'Некорректный ввод (нужно два натуральных числа через пробел).\n'
                                               'Введите диапазон цен ещё раз')
        return
    min_price = min(price_range_list)
    max_price = max(price_range_list)
    price_range = '-'.join(price_range_list)

    with bot.retrieve_data(message.from_user.id) as data:
        product_name = data['new_custom']['product_name']
        result_size = data['new_custom']['result_size']
    History.create(  # Записываем вызов команды в базу данных
        search_time=datetime.now(),
        user=message.from_user.id,
        command_name='custom',
        product_name=product_name,
        result_size=result_size,
        price_range=price_range
    ).save()

    # TODO Написать код, обрабатывающий запрос поиска товаров в AmazonAPI.
    # amazon_search = site_api.search_products()
    # response = amazon_search(url, 'iphone', headers, params)
    result = 'Те самые товары с Амазон по команде /custom'
    bot.send_message(message.from_user.id, result)
    bot.delete_state(message.from_user.id)  # Убираем состояние
