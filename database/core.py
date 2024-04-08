from database.utils.CRUD import CRUDInterface
from database.common.models import db, BaseModel

db.connect()
db.create_tables(BaseModel.__subclasses__())

crud = CRUDInterface()


if __name__ == '__main__':
    crud()
