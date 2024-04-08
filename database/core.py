from database.common.models import db, BaseModel

db.connect()
db.create_tables(BaseModel.__subclasses__())
