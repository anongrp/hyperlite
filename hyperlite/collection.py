"""   Contains Information of the Collection   """

from .database import Database

class Collection:

    def __init__(self, col_name: str, parent: Database):
        self.col_name = col_name
        self.objects = {}
        self.col_id = Collections.generate_id(self)
        self.parent = parent

    def __str__(self):
        return self.col_name

    def insert(self, collection_id: str, user_data: dict):
        collection = Collections.get_collection(collection_id)
        object_id = Objects.generate_id(collection)
        collection.objects.update({
            object_id: user_data
        })
        return object_id

    def update(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def meta_separator(cls, meta_data: dict) -> list:
        return [meta for meta in meta_data.values()]


class Collections:
    """   Maintains record of all Collections   """
    collection_list = {}

    @classmethod
    def generate_id(cls, collection: Collection) -> str:
        col_id = ''
        Collections.collection_list.update({
            col_id: collection
        })
        return col_id

    @classmethod
    def get_collection(cls, col_id: str):
        collection = Collections.collection_list.get(col_id)
        return collection


class Objects:
    """    Helps to Maintain record of all Objects"""

    @classmethod
    def generate_id(cls, collection: Collection) -> str:
        obj_id = ''
        return obj_id
