"""   Contains Information of the Database   """

from time import gmtime, strftime

class Database:

    def __init__(self, __db_name: str, __collections: dict = {}):
        self.__db_name = __db_name
        self.__collections = __collections
        self.__creation_date: str = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def __str__(self):
        return self.__db_name+'\n'+str(self.__creation_date)

    def getDBName(self):
        return self.__db_name
    
    def setDBName(self, __db_name):
        self.__db_name = __db_name

    def getCreationDetails(self):
        return self.__creation_date

    def getCollections(self):
        return list(self.__collections.keys())
    
    def getCollectionInfo(self, collection_name: str):
        return dict['collection_name']
    
    def dropDatabase(self):
        pass
    
    def addCollection(*args, **kwargs):
        pass