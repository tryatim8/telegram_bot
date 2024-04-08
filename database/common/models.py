from datetime import datetime
from peewee import (SqliteDatabase, Model, IntegerField, AutoField,
                    ForeignKeyField, DateTimeField, TextField)

db = SqliteDatabase('client.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)  # Первичный ключ модели, будет совпадать с Telegram ID, уникален.
    username = TextField()  # Никнейм в telegram
    first_name = TextField()  # Имя в telegram
    last_name = TextField(null=True)  # Фамилия в telegram. Может быть не указана, поэтому ставим null=True.


class History(BaseModel):
    command_ord = AutoField()  # Автоматический ID. Это порядковый номер команды.
    search_time = DateTimeField(default=datetime.now())  # Время запроса
    user = ForeignKeyField(User, backref='search_history')  # Привязка истории к пользователю
    command_name = TextField()  # Имя команды
    query_name = TextField(null=True)  # Текст запроса (Название товара или его код)
    price_range = TextField(null=True)  # Диапазон цен (команда custom)
