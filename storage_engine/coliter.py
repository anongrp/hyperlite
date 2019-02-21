import _pickle
from hyperlite import config
from hyperlite.collection import Collection, Database


def writer(collection: Collection):
    _pickle.dump(collection, open(__getCollectionUri(collection), "wb"))


def __getCollectionUri(collection: Collection) -> str:
    return config.DATABASE_PATH + __getPathSeparator() + collection.parent.name + __getPathSeparator() + collection.col_name + "." + config.DATABASE_FORMAT['type']


def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
