from datetime import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField, DateTimeField

db = SqliteDatabase('client.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)  # Первичный ключ модели, будет совпадать с Telegram ID, уникален.
    username = CharField()  # Никнейм в telegram
    first_name = CharField()  # Имя в telegram
    last_name = CharField(null=True)  # Фамилия в telegram. Может быть не указана, поэтому ставим null=True.


class History(BaseModel):
    try_id = AutoField()  # Автоматический ID. Это номер результата.
    search_time = DateTimeField(default=datetime.now())  # Время запроса
    user = ForeignKeyField(User, backref='search_history')  # Бэкреф к пользователю
    product_name = CharField()  # Имя товара
    product_price = CharField()  # Цена товара
    product_url = CharField()  # Ссылка на товар
