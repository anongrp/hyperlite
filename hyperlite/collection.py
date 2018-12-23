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
    
    def addCol(self,col_name: str):
        self.columns.append(col_name)
    
    def dropCollection(self):
        pass