from database.common.models import BaseModel, db


def create_tables() -> None:
    """Инициализация БД и создание таблиц."""
    db.connect()
    db.create_tables(BaseModel.__subclasses__())
