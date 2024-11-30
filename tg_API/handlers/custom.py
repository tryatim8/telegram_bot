from datetime import datetime
from typing import Dict, List

from config import RESULT_LIMIT
from database.common.models import History, User
from site_API.core import headers, params, site_api, url
from tg_API.core import bot
from tg_API.states import UserState


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
    bot.send_message(message.from_user.id, 'Введите количество товаров, до 15 штук')
    bot.set_state(message.from_user.id, UserState.custom_result_size)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_custom']['product_name'] = product_name


@bot.message_handler(state=UserState.custom_result_size)
def handle_custom_result_size(message) -> None:
    try:
        result_size = min(int(message.text), RESULT_LIMIT)
        if result_size <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.from_user.id, 'Некорректный ввод (нужно натуральное число).\n'
                                               'Введите количество товаров ещё раз')
        return
    bot.send_message(message.from_user.id, 'Введите диапазон цен (EUR) через пробел')
    bot.set_state(message.from_user.id, UserState.custom_price_range)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_custom']['result_size'] = result_size


@bot.message_handler(state=UserState.custom_price_range)
def handle_custom_price_range(message) -> None:
    price_range_str = message.text
    try:
        price_range_list = list(map(int, price_range_str.split(' ')[:2]))
        min_price = min(price_range_list)
        max_price = max(price_range_list)
        if min_price <= 0 or max_price <= 0:
            raise ValueError
    except (ValueError, IndexError):
        bot.send_message(message.from_user.id, 'Некорректный ввод (нужно два натуральных числа через пробел).\n'
                                               'Введите диапазон цен ещё раз')
        return
    price_range = '-'.join(map(str, price_range_list))

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

    amazon_search = site_api.search_products()  # Функция для поиска товаров
    response = amazon_search(url, product_name, headers, params)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, 'Запрос не выполнен успешно. Попробуйте позже')
        bot.delete_state(message.from_user.id)  # Убираем состояние
        return
    response_data: List[Dict] = list(response.json()['result'])
    changed_data = list(filter(lambda elem: min_price <= elem['price']['current_price'] <= max_price, response_data))
    if not changed_data:
        bot.send_message(message.from_user.id, 'Ничего не найдено')
        bot.delete_state(message.from_user.id)  # Убираем состояние
        return
    for i_ord, i_dict in enumerate(changed_data):
        product = (
            f'{i_ord + 1}-й товар:\n'
            f'asin - ID: {i_dict['asin']}\n'
            f'Цена без скидки: {i_dict['price']['before_price']}\n'
            f'Скидка: {i_dict['price']['savings_percent']} %\n'
            f'Цена со скидкой: {i_dict['price']['current_price']}\n'
            f'Рейтинг: {i_dict['reviews']['rating']}\n'
            f'Валюта: {i_dict['price']['currency']}\n'
            f'URL-ссылка: {i_dict['url']}\n'
        )
        bot.send_message(message.from_user.id, product)
        if i_ord == result_size-1:
            break
    bot.delete_state(message.from_user.id)  # Убираем состояние
