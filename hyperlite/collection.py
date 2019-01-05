"""   Contains Information of the Collection   """

from .database import Database

class Collection:
    
    def __init__(self, name: str, parent: Database):
        self.name = name
        self.objects = []
        self.parent = parent


    # def insert(self, meta_data: dict, user_data: dict):
    #     Database, Collection = self.__meta_separator(meta_data)
    #     pass
    #
    #
    # def __meta_separator(self, meta_data: dict) -> list:
    #     return [meta for meta in meta_data.values()]
