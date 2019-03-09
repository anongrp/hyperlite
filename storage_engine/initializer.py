import _pickle
from hyperlite.logger import Log

TAG = "Collection_Reader"


def getCollection(path):
    Log.d(TAG, f"Getting a collection from {path}")
    try:
        return _pickle.load(open(path, 'rb'))
    except Exception as ex:
        Log.w(TAG, "Someone explicitly deleted the collection file from disk")
        Log.e(TAG, f"Collection is not exist on {path}. {ex}")
        return None


# def getCollections(database: Database):
#     collections = []
#     database_dir = config.DATABASE_PATH + __getPathSeparator() + database.name
#     collection_files = os.listdir(database_dir)
#     for collection_file in collection_files:
#         collection_path = os.path.join(database_dir, collection_file)
#         collections.append(_pickle.load(open(collection_path, 'rb')))
#     return collections
