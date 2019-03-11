import _pickle
import time
from hyperlite import config
from hyperlite.logger import Log
from hyperql.parser import parser
from hyperlite.event import Event
from hyperlite.collection import Collection

TAG = "StorageEngine Provider"


class Provider(object):
    collection_list = {}
    meta_collection = None

    @classmethod
    def create_new_collection(cls, col_name, db_name):
        new_collection = Collection(col_name, db_name)
        Provider.add_collection(new_collection)
        Provider.meta_collection.insert({
            "db_name": db_name,
            "col_name": col_name,
            "time_stamp": parserTimeStamp(str(time.time())),  # its helps to find this collection on disk
            "user": "Anonymous"
        })
        Event.emmit('col-change', Provider.meta_collection)
        return new_collection

    @classmethod
    def add_collection(cls, collection: Collection):
        if Provider.collection_list.get(collection.parent) is not None:
            Provider.collection_list.get(collection.parent).add(collection)
        else:
            Provider.collection_list.update({
                collection.parent: {collection}
            })

    @classmethod
    def get_collection(cls, col_name: str, db_name):
        if Provider.collection_list.get(db_name) is not None:
            database = Provider.collection_list.get(db_name)
            result_col = None
            for collection in database:
                if col_name == collection.col_name:
                    result_col = collection
                    break
            if result_col is not None:
                print("Getting collection from ram")
                return result_col
            else:
                # Fetching or create new Collection
                print("Fetching or create new Collection")
                query = f"""
                            time_stamp,
                            db_name &eq "{db_name}",
                            col_name &eq "{col_name}"
                            """
                result = Provider.meta_collection.readOne(parser(query))
                if not result:
                    print("Getting new collection because collection is not in ram and also on a disk")
                    return Provider.create_new_collection(col_name, db_name)
                else:
                    result = result[0]
                    print("Getting collection from disk")
                    result = loadCollection(
                        config.DATABASE_PATH + getPathSeparator() + str(result.get("time_stamp")) + ".col")
                    Provider.add_collection(result)
                    return result
        else:
            query = f"""
                        time_stamp,
                        db_name &eq "{db_name}",
                        col_name &eq "{col_name}"
                        """
            result = Provider.meta_collection.readOne(parser(query))
            if not result:
                print("Getting new collection: @no database found")
                return Provider.create_new_collection(col_name, db_name)
            else:
                result = result[0]
                print("Getting collection from disk: @root else")
                result = loadCollection(
                    config.DATABASE_PATH + getPathSeparator() + str(result.get('time_stamp')) + ".col")
                Provider.add_collection(result)
                return result


def loadCollection(path):
    Log.d(TAG, f"Getting a collection from {path}")
    try:
        return _pickle.load(open(path, 'rb'))
    except Exception as ex:
        Log.w(TAG, "Someone explicitly deleted the collection file from disk")
        Log.e(TAG, f"Collection is not exist on {path}. {ex}")
        return None


def parserTimeStamp(time_stamp):
    return time_stamp[0: time_stamp.find('.')]


def getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
