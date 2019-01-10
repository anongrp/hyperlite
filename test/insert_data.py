from hyperlite.database import Database
from hyperlite.collection import Collection
from hyperlite.request_parser import Parser
from hyperlite.process import Process


with open('test2.json', 'r') as f1:
    data = f1.read()


db = Database('db-1')
col = Collection('col-1', db)
data = Parser.parse(data)
process1 = Process(data)
process1.exec()

print(col.objects)