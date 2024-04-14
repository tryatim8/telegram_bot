from database.common.models import db, BaseModel


def create_tables():
    db.connect()
    db.create_tables(BaseModel.__subclasses__())
