import _pickle
from hyperlite import config
from hyperlite.collection import Collection

import os
import time
from hyperlite import collection


def writer(collection: Collection):
    try:
        print(collection)
        doctor()
        _pickle.dump(collection, open(__getNewCollectionUri(), "wb"))
        print("Saved to disk")
        return True
    except Exception as ex:
        print("Error in collection writer")
        return False


def doctor():
    if not os.path.exists(config.DATABASE_PATH):
        os.makedirs(config.DATABASE_PATH)   # mkdir() for just one folder, makedirs() for creating multiple folders


def __getNewCollectionUri() -> str:
    return config.DATABASE_PATH + __getPathSeparator() + __generateColFileName()


def __generateColFileName() -> str:
    name = str(time.time())
    return name[0: name.find('.')] + name[name.find('.'): len(name)] + "." + config.DATABASE_FORMAT["type"]


def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
