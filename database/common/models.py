from peewee import (
    AutoField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

from config import DATETIME_FORMAT

db = SqliteDatabase('client.db')


class BaseModel(Model):
    """Базовая модель peewee."""

    class Meta:
        """Привязка метаданных к объекту БД."""

        database = db


class User(BaseModel):
    """Таблица пользователей."""

    user_id = IntegerField(primary_key=True)  # Первичный ключ Telegram ID
    user_name = TextField(null=True)  # Никнейм в telegram
    first_name = TextField()  # Имя в telegram
    last_name = TextField(null=True)  # Фамилия в telegram опционально.


class History(BaseModel):
    """Таблица истории команд."""

    command_order = AutoField()  # Автоматический ID. Порядковый номер команды.
    search_time = DateTimeField()  # Время запроса
    user = ForeignKeyField(User, backref='commands_history')  # Привязка
    command_name = TextField()  # Имя команды
    product_name = TextField(null=True)  # Текст запроса (Название или код)
    result_size = IntegerField(null=True)  # Количество предложенных товаров
    price_range = TextField(null=True)  # Диапазон цен (команда custom)

    def __str__(self):
        """Строковое представление записи истории команд."""
        return (
            '{num} - {dtime}, /{comm}, a-{name}, b-{limit}, c-{range}'
        ).format(
            num=self.command_order,
            dtime=self.search_time.strftime(DATETIME_FORMAT),
            comm=self.command_name,
            name=self.product_name,
            limit=self.result_size,
            range=self.price_range,
        )
