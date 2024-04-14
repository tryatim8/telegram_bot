from datetime import datetime
from typing import List, Dict

from tg_API.core import bot
from database.common.models import User, History
from tg_API.states import UserState
from site_API.core import site_api, url, headers, params
from config import RESULT_LIMIT


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
    bot.send_message(message.from_user.id, 'Введите количество товаров, до 15 штук')
    bot.set_state(message.from_user.id, UserState.high_result_size)
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_high']['product_name'] = product_name


@bot.message_handler(state=UserState.high_result_size)
def handle_high_result_size(message) -> None:
    try:
        result_size = min(int(message.text), RESULT_LIMIT)
        if result_size <= 0:
            raise ValueError
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

    amazon_search = site_api.search_products()  # Функция для поиска товаров
    response = amazon_search(url, product_name, headers, params)
    if response.status_code != 200:
        bot.send_message(message.from_user.id, 'Запрос не выполнен успешно. Попробуйте позже')
        bot.delete_state(message.from_user.id)  # Убираем состояние
        return
    response_data: List[Dict] = sorted(response.json()['result'],
                                       key=lambda x: x['price']['current_price'], reverse=True)
    for i_ord, i_dict in enumerate(response_data):
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
