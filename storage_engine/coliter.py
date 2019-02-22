import _pickle
from hyperlite import config
from hyperlite.collection import Collection

import sys
sys.path.append('..')
import _pickle
from hyperlite import config
from hyperlite.collection import Collection

import os
from hyperlite import process
from hyperlite import request_parser
from hyperlite import database
from hyperlite import collection
import bson


class Store(): 

    @staticmethod
    def __getPathSeparator() -> str:
        return "/" if config.PLATFORM == "Linux" else r"\\"

    @staticmethod
    def Store_this(col: collection, dat):

        col = col
        data = bson.BSON.encode(dat.user_data)

        try:
            print("Setting route")
            print("*"*20)

            print(os.path.dirname(os.path.realpath(__file__)))
            db_route = os.path.dirname(
                os.path.realpath(__file__)) + "\\" + col.parent.db_name
            
            print(db_route)
            os.mkdir(db_route)

            file_uri = db_route + "\\" + str(col) + ".bson"
            
            print(file_uri)
            
            print("Dumping data")
            print("*"*20)

            _pickle.dump(data, open(file_uri), "wb")

            print("file has been successfully stored")


        except (FileExistsError, FileNotFoundError) as e:

            print("Some exception occured or path alredy exists")

            file_uri = db_route + "\\" + str(col) + ".bson"

            print(file_uri)

            print("Dumping data with exception")
            print("*"*20)

            _pickle.dump(data, open(file_uri, "wb"), 0)

            print("file has been successfully stored")

    
    @staticmethod 
    def Fetch_this(col: collection):
        col = col
        dbname = col.parent.db_name
        colName = str(col)
        

        file_route = os.path.dirname(
            os.path.realpath(__file__)) + "\\" + dbname + "\\" + colName + '.bson'

        print(file_route)
        print('-'*30)

        with open(file_route, 'rb') as raw_bson:
            file = raw_bson.read()

        print(file)
        print('-'*30)

        print(type(file))

        






    @staticmethod
    def create_db_folder(collection):
        col = collection
        dbname = str(col.parent)
        colName = str(col)

        

        

   
#anikesh


def writer(collection: Collection):
    try:
        _pickle.dump(collection, open(__getCollectionUri(collection), "wb"))
        return True
    except Exception as ex:
        return False


def __getCollectionUri(collection: Collection) -> str:
    return config.DATABASE_PATH + __getPathSeparator() + collection.parent.name + __getPathSeparator() + collection.col_name + "." + \
           config.DATABASE_FORMAT['type']


def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
