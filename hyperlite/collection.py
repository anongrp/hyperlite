"""   Contains Information of the Collection   """

class Collection:
    
    def __init__(self, __tb_name: str):
        self.__tb_name=__tb_name
        self.columns = []

    def __str__(self):
        return self.__tb_name

    def setTBName(self,__tb_name: str):
        self.__tb_name=__tb_name

    def getTBName(self):
        return self.__tb_name
    
    def insert(self,meta_data: dict, user_data: dict):
        Database, Collection = self.__meta_separator(meta_data)
        pass
    
    def __meta_separator(self, meta_data: dict) -> list:
        return [meta for meta in meta_data.values()]

    def dropCollection(self):
        pass