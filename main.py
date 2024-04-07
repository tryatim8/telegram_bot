import telebot
from telebot.types import Message

from config import ConfigSettings

config = ConfigSettings()

bot = telebot.TeleBot(config.bot_token.get_secret_value())


@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    bot.send_message(message.chat.id, 'Добрый день, {}!'.format(message.from_user.first_name))


@bot.message_handler(commands=['help'])
def handle_start(message: Message) -> None:
    bot.send_message(message.chat.id, '/start - Начало работы\n/hello_world - Привет мир\n'
                                      'Ввести "Привет" - приветствие')


@bot.message_handler(commands=['hello_world'])
def send_hello_world(message):
    bot.send_message(message.chat.id, 'Hello World!')


@bot.message_handler(func=lambda message: message.text.title() == 'Привет')
def hello_info(message):
    bot.send_message(message.chat.id, 'Вас приветствует чат-бот поиска товаров интернет-магазина\n'
                                      'Для получения списка команд отправьте /help')


@bot.message_handler(func=lambda message: True)
def echo_and_info(message):
    bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, 'Для начала работы отправьте слово Привет')


if __name__ == '__main__':
    bot.infinity_polling()
