import _pickle
import multiprocessing
from hyperlite import config
from hyperql import parser
from hyperlite.collection import Collection, Collections
from hyperlite.logger import Log

import os
import time

TAG = "Storage_Engine"


def postWriter(collection: Collection):
    multiprocessing.Process(target=writer, args=[collection]).start()


def writer(collection):
    try:
        doctor()
        if collection is list:
            for col in collection:
                if col.col_name == config.DEFAULT_META_COLLECTION_NAME:
                    _pickle.dump(col, open(config.COLLECTION_PATH, "wb"))
                    Log.d(TAG, f"{collection.col_name} written on disk")
                else:
                    _pickle.dump(col, open(__getNewCollectionUri(col), "wb"))
                    Log.d(TAG, f"{collection.col_name} written on disk")
        else:
            if collection.col_name == config.DEFAULT_META_COLLECTION_NAME:
                _pickle.dump(collection, open(config.COLLECTION_PATH, "wb"))
                Log.d(TAG, f"{collection.col_name} written on disk")
            else:
                _pickle.dump(collection, open(__getNewCollectionUri(collection), "wb"))
                Log.d(TAG, f"{collection.col_name} written on disk")
        return True
    except Exception as ex:
        Log.e(TAG, f"Enable to write {collection.col_name} collection on disk")
        return False


def doctor():
    if not os.path.exists(config.DATABASE_PATH):
        Log.w(TAG, "Database directory does not exist")
        os.makedirs(config.DATABASE_PATH)
        Log.i(TAG, "Database directory Created")


def __getNewCollectionUri(collection: Collection) -> str:
    return config.DATABASE_PATH + __getPathSeparator() + __getCollectionNameForDisk(collection) + "." + config.DATABASE_FORMAT.get('type')


def __generateColFileName() -> str:
    name = str(time.time())
    return name[0: name.find('.')] + name[name.find('.'): len(name)] + "." + config.DATABASE_FORMAT["type"]


def __getCollectionNameForDisk(collection: Collection) -> str:
    query = f""" 
            time_stamp,
            db_name &eq "{collection.parent}", 
            col_name &eq "{collection.col_name}"
            """
    Log.d(TAG, "Searching collection name for disk")
    data = Collections.meta_collection.readOne(parser.parser(query))[0]
    Log.d(TAG, f"Collection name for disk is {data}")
    Log.d(TAG, f"{data.get('time_stamp')}.col")
    return str(data.get("time_stamp"))


def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
