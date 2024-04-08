import telebot
from config import ConfigSettings

config = ConfigSettings()

bot = telebot.TeleBot(config.bot_token.get_secret_value())
