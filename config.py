import os

from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings

load_dotenv()

DATETIME_FORMAT = '%d.%m.%Y - %H:%M:%S'
DEFAULT_COMMANDS = (
    ('start', 'Начало работы'),
    ('help', 'Информация по командам'),
    ('low', 'Предложить товары/услуги по минимальным характеристикам поиска'),
    ('high', 'Предложить товары/услуги по максимальным характеристикам поиска'),
    ('custom', 'Предложить товары/услуги по настраиваемым характеристикам поиска'),
    ('history', 'История поиска')
)
RESULT_LIMIT = 15


class ConfigSettings(BaseSettings):
    bot_token: SecretStr = os.getenv('BOT_TOKEN', None)
    api_key: SecretStr = os.getenv('SITE_API', None)
    host_api: StrictStr = os.getenv('HOST_API', None)
