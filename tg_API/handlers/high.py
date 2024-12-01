from datetime import datetime
from typing import Dict, List

from config import RESULT_LIMIT
from database.common.models import History, User
from site_API.core import headers, params, site_api, url
from tg_API.core import bot
from tg_API.states import UserState


@bot.message_handler(commands=['high'])
def handle_high(message) -> None:
    """Хэндлер команды high. Проверяет, зарегистрирован ли пользователь."""
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы. Напишите /start')
        return
    bot.send_message(message.from_user.id, 'Введите название товара.')
    bot.set_state(message.from_user.id, UserState.high_prod_name)
    with bot.retrieve_data(message.from_user.id) as user_data:
        user_data['new_high'] = {'user_id': user_id}


@bot.message_handler(state=UserState.high_prod_name)
def handle_high_prod_name(message) -> None:
    """Хэндлер сообщения для поиска по верхнему пределу числа товаров."""
    product_name = message.text
    bot.send_message(
        message.from_user.id,
        'Введите количество товаров, до 15 штук',
    )
    bot.set_state(message.from_user.id, UserState.high_result_size)
    with bot.retrieve_data(message.from_user.id) as user_data:
        user_data['new_high']['product_name'] = product_name


@bot.message_handler(state=UserState.high_result_size)
def handle_high_result_size(message) -> None:
    """Хэндлер сообщений для поиска товаров по числу результатов."""
    result_size = min(int(message.text), RESULT_LIMIT)
    try:
        if result_size <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(
            message.from_user.id,
            'Некорректный ввод (нужно натуральное число).\n' +
            'Введите количество товаров ещё раз',
        )
        return
    with bot.retrieve_data(message.from_user.id) as user_data:
        product_name = user_data['new_high']['product_name']
    History.create(  # Записываем вызов команды в базу данных
        search_time=datetime.now(),
        user=message.from_user.id,
        command_name='high',
        product_name=product_name,
        result_size=result_size,
    ).save()
    search_and_send(message, product_name, result_size)


def search_and_send(message, product_name, result_size):
    """Функция поиска товаров и отправки результатов пользователю."""
    amazon_search = site_api.search_products()  # Функция для поиска товаров
    response = amazon_search(url, product_name, headers, params)
    resp_ok_code = 200
    if response.status_code != resp_ok_code:
        bot.send_message(
            message.from_user.id,
            'Запрос не выполнен успешно. Попробуйте позже',
        )
        bot.delete_state(message.from_user.id)  # Убираем состояние
        return
    response_data: List[Dict] = sorted(
        response.json()['result'],
        key=lambda prod: prod['price']['current_price'],
        reverse=True,
    )
    for i_ord, i_dict in enumerate(response_data):
        product = (
            '{0}-й товар:\n'.format(i_ord + 1) +
            'asin - ID: {0}\n'.format(i_dict['asin']) +
            'Цена без скидки: {0}\n'.format(i_dict['price']['before_price']) +
            'Скидка: {0} %\n'.format(i_dict['price']['savings_percent']) +
            'Цена со скидкой: {0}\n'.format(i_dict['price']['current_price']) +
            'Рейтинг: {0}\n'.format(i_dict['reviews']['rating']) +
            'Валюта: {0}\n'.format(i_dict['price']['currency']) +
            'URL-ссылка: {0}\n'.format(i_dict['url']),
        )
        bot.send_message(message.from_user.id, product)
        if i_ord == result_size - 1:
            break
    bot.delete_state(message.from_user.id)  # Убираем состояние
