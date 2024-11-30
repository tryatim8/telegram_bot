from database.common.models import BaseModel, db


def create_tables():
    db.connect()
    db.create_tables(BaseModel.__subclasses__())
