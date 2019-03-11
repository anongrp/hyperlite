from storage_engine import coliter
from storage_engine.provider import Provider
from ..collection import Collection
from hyperql import parser
from ..event import Event
from hyperlite.logger import Log

TAG = "Process_API"


class Process(object):
    def exec(self):
        pass


class BaseRIDUProcess(Process):
    @staticmethod
    def meta_separator(meta_data: dict) -> list:
        return [meta for meta in meta_data.values()]


class WriteProcess(Process):
    def __init__(self, collection: Collection):
        self.collection = collection

    def exec(self) -> bool:
        return coliter.writer(self.collection)


class DefragProcess(Process):
    def __init__(self, collection: Collection):
        self.collection = collection

    def exec(self) -> Collection:
        pass


class EncryptionProcess(Process):
    def __init__(self, collection: Collection):
        self.collection = collection

    def exec(self) -> Collection:
        pass


class ReadProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "ReadProcess created.")

    def exec(self):
        Log.i(TAG, "Executing ReadProcess.")
        db_name, col_name, query = BaseRIDUProcess.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        query_object = parser.parser(query)
        return {
            "Ack": col.read(query_object),
            "addr": self.data.addr
        }


class InsertProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "InsertProcess created.")

    def exec(self):
        Log.i(TAG, "Executing InsertProcess.")
        db_name, col_name = BaseRIDUProcess.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.insert(self.data.user_data),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class UpdateProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "UpdateProcess created.")

    def exec(self):
        Log.i(TAG, "Executing UpdateProcess.")
        db_name, col_name, query = Collection.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        query_object = parser.parser(query)
        acknowledgement = {
            "Ack": col.updateAll(query_object, self.data.user_data),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class DeleteProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "DeleteProcess created.")

    def exec(self):
        Log.i(TAG, "Executing DeleteProcess.")
        db_name, col_name, object_id = Collection.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.delete(object_id),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class ReadOneProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "ReadOneProcess created.")

    def exec(self):
        Log.i(TAG, "Executing ReadOneProcess.")
        db_name, col_name, query = BaseRIDUProcess.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        query_object = parser.parser(query)
        return {
            "Ack": col.readOne(query_object),
            "addr": self.data.addr
        }


class UpdateOneProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "UpdateOneProcess created.")

    def exec(self):
        Log.i(TAG, "Executing UpdateOneProcess.")
        db_name, col_name, object_id = Collection.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.updateOne(object_id, self.data.user_data),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class ReadByIdProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data
        Log.i(TAG, "ReadByIdProcess created.")

    def exec(self):
        Log.i(TAG, "Executing ReadByIdProcess.")
        db_name, col_name, object_id = Collection.meta_separator(self.data.meta_data)
        col = Provider.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.findById(object_id),
            "addr": self.data.addr
        }
        return acknowledgement


class DataPipelineProcess(Process):
    def __init__(self, data):
        self.data = data
        self.output = []
        Log.i(TAG, "DataPipelineProcess created.")

    def exec(self):
        Log.i(TAG, "Executing DataPipelineProcess.")
        database = self.data.get('Database')
        mainColName = self.data.get('Collection')
        targetColName = self.data.get('to')
        fieldAddress = self.data.get('fieldRef')

        mainCollection = Provider.get_collection(mainColName, database)
        targetCollection = Provider.get_collection(targetColName, database)
        references = mainCollection.read(parser.parser(f"{fieldAddress}"))
        ref_key = DataPipelineProcess.getLastFieldSegment(fieldAddress)
        print(mainCollection.read(parser.parser(self.data.get('query'))))
        for reference in references:
            if type(reference.get(ref_key)) is list:
                for ref in reference.get(ref_key):
                    self.output.append(targetCollection
                                       .findById(ref))
            else:
                self.output = targetCollection \
                    .findById(reference.get(ref_key))

        acknowledgement = {
            "Ack": self.output,
            "addr": self.data.get('addr')
        }
        return acknowledgement

    @staticmethod
    def getLastFieldSegment(fieldRef):
        return fieldRef.split('.')[-1]


def renderRIDUProcess(parsed_data):
    Log.i(TAG, "Rendering Process...")
    if parsed_data.request_type == 'Read':
        return ReadProcess(parsed_data)
    elif parsed_data.request_type == 'Update':
        return UpdateProcess(parsed_data)
    elif parsed_data.request_type == 'Insert':
        return InsertProcess(parsed_data)
    elif parsed_data.request_type == 'Delete':
        return DeleteProcess(parsed_data)
    elif parsed_data.request_type == 'ReadById':
        return ReadByIdProcess(parsed_data)
    elif parsed_data.request_type == 'ReadOne':
        return ReadOneProcess(parsed_data)
    elif parsed_data.request_type == 'UpdateOne':
        return UpdateOneProcess(parsed_data)
    else:
        Log.e(TAG, "No compatible request_type found.")
        return None


def renderProcess(collection: Collection):
    process = []
    # if _shouldDefrag():
    #     process.append(DefragProcess(collection))
    # process.append(EncryptionProcess(collection))
    process.append(WriteProcess(collection))
    return process


def _shouldDefrag() -> bool:
    pass
