from config import DATETIME_FORMAT

from peewee import (SqliteDatabase, Model, IntegerField, AutoField,
                    ForeignKeyField, DateTimeField, TextField)

db = SqliteDatabase('client.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)  # Первичный ключ модели, будет совпадать с Telegram ID, уникален.
    user_name = TextField(null=True)  # Никнейм в telegram
    first_name = TextField()  # Имя в telegram
    last_name = TextField(null=True)  # Фамилия в telegram. Может быть не указана, поэтому ставим null=True.


class History(BaseModel):
    command_order = AutoField()  # Автоматический ID. Это порядковый номер команды.
    search_time = DateTimeField()  # Время запроса
    user = ForeignKeyField(User, backref='commands_history')  # Привязка истории к пользователю
    command_name = TextField()  # Имя команды
    query_name = TextField(null=True)  # Текст запроса (Название товара или его код)
    result_size = IntegerField(null=True)  # Количество предложенных товаров
    price_range = TextField(null=True)  # Диапазон цен (команда custom)

    def __str__(self):
        return '{num} - {dtime}, /{comm}, a-{name}, b-{limit}, c-{range}'.format(
            num=self.command_order,
            dtime=self.search_time.strftime(DATETIME_FORMAT),
            comm=self.command_name,
            name=self.query_name,
            limit=self.result_size,
            range=self.price_range
        )
