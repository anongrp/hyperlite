import sys
sys.path.append('..')
from hyperlite.database import Database
from hyperlite.collection import Collection
from hyperlite.request_parser import Parser
from hyperlite.process import Process


with open('test2.json', 'r') as f1:    #taking the user's data file to store 
    data = f1.read()


db = Database('db-1')               #object of database class
col = Collection('col-1', db)       
data = Parser.parse(data)           #parsing data, extracting the info and commands from data file
process1 = Process(data)
process1.exec()                     #finally execute the given command given by user

print(col.objects)
