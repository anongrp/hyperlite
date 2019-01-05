import _pickle
import os
from hyperlite import config
from hyperlite.collection import Collection, Database


def getCollections(database: Database):
    collections = []
    database_dir = config.DATABASE_PATH + __getPathSeparator() + database.name
    collection_files = os.listdir(database_dir)
    for collection_file in collection_files:
        collection_path = os.path.join(database_dir, collection_file)
        collections.append(_pickle.load(open(collection_path, 'rb')))
    return collections

def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
