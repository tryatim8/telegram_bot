from telebot.custom_filters import StateFilter
from telebot.types import BotCommand

from tg_API.core import bot
from config import DEFAULT_COMMANDS
from database.core import create_tables
from tg_API.handlers import start, help, low, high, custom, history, echo

if __name__ == '__main__':
    create_tables()
    bot.add_custom_filter(StateFilter(bot))
    bot.set_my_commands([BotCommand(*cmd) for cmd in DEFAULT_COMMANDS])
    bot.infinity_polling()
