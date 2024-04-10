from tg_API.core import bot
import database.core
from tg_API.handlers import start, help, low, high, custom, history, echo

if __name__ == '__main__':
    bot.infinity_polling()
