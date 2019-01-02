"""   Contains Information of the Collection   """

class Collection:
    
    def __init__(self, col_name: str):
        self.col_name = col_name
        self.objects = []

    def __str__(self):
        return self.col_name

    def setTBName(self, col_name: str):
        self.col_name = col_name

    def getTBName(self):
        return self.col_name
    
    def insert(self,meta_data: dict, user_data: dict):
        Database, Collection = self.__meta_separator(meta_data)
        for(collection in db.getCollections()):
            if collection == Collection:
                pass
            else:
                pass        
    
    
    def __meta_separator(self, meta_data: dict) -> list:
        return [meta for meta in meta_data.values()]

    def dropCollection(self):
        pass