from typing import Dict, List, TypeVar
from peewee import ModelSelect

from database.common.models import db, BaseModel

T = TypeVar('T')


def _store_date(db: db, model: T, *data: List[Dict]) -> None:
    with db.atomic():
        model.insert_many(*data).execute()


def _retrieve_all_data(db: db, model: T, *columns: BaseModel) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)

    return response


class CRUDInterface:
    @classmethod
    def create(cls):
        return _store_date

    @classmethod
    def retrieve(cls):
        return _retrieve_all_data


if __name__ == '__main__':
    _store_date()
    _retrieve_all_data()
    CRUDInterface()
