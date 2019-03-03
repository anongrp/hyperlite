import _pickle
import multiprocessing
from hyperlite import config
from hyperlite.collection import Collection

import os
import time


def postWriter(collection: Collection):
    multiprocessing.Process(target=writer, args=[collection]).start()


def writer(collection):
    try:
        doctor()
        if collection is list:
            for col in collection:
                if col.col_name == config.DEFAULT_META_COLLECTION_NAME:
                    _pickle.dump(col, open(config.COLLECTION_PATH, "wb"))
                else:
                    _pickle.dump(col, open(__getNewCollectionUri(), "wb"))
        else:
            if collection.col_name == config.DEFAULT_META_COLLECTION_NAME:
                _pickle.dump(collection, open(config.COLLECTION_PATH, "wb"))
            else:
                _pickle.dump(collection, open(__getNewCollectionUri(), "wb"))
        return True
    except Exception as ex:
        return False


def doctor():
    if not os.path.exists(config.DATABASE_PATH):
        os.makedirs(config.DATABASE_PATH)


def __getNewCollectionUri() -> str:
    return config.DATABASE_PATH + __getPathSeparator() + __generateColFileName()


def __generateColFileName() -> str:
    name = str(time.time())
    return name[0: name.find('.')] + name[name.find('.'): len(name)] + "." + config.DATABASE_FORMAT["type"]


def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
