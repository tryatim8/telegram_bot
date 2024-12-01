import os

from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings

load_dotenv()

DATETIME_FORMAT = '%d.%m.%Y - %H:%M:%S'
DEFAULT_COMMANDS = (
    ('start', 'Начало работы'),
    ('help', 'Информация по командам'),
    ('low', 'Товары/услуги по минимальным характеристикам поиска'),
    ('high', 'Товары/услуги по максимальным характеристикам поиска'),
    ('custom', 'Товары/услуги по настраиваемым характеристикам поиска'),
    ('history', 'История поиска'),
)
RESULT_LIMIT = 15


class ConfigSettings(BaseSettings):
    """Модель базовых настроек pydantic-settings чувствительных переменных."""

    bot_token: SecretStr = os.getenv('BOT_TOKEN', None)
    api_key: SecretStr = os.getenv('SITE_API', None)
    host_api: StrictStr = os.getenv('HOST_API', None)
