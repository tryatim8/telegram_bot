from telebot.handler_backends import StatesGroup, State


class UserState(StatesGroup):  # Группа состояний
    low_prod_name = State()
    low_result_size = State()
    high_prod_name = State()
    high_result_size = State()
    custom_prod_name = State()
    custom_price_range = State()
    custom_result_size = State()
