from storage_engine import coliter
from ..collection import Collection, Collections
from hyperql import parser
from ..event import Event


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

    def exec(self):
        db_name, col_name, query = BaseRIDUProcess.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        query_object = parser.hyperql_parser(query)
        return {
            "Ack": col.read(query_object),
            "addr": self.data.addr
        }


class InsertProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data

    def exec(self):
        db_name, col_name = BaseRIDUProcess.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.insert(self.data.user_data),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class UpdateProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data

    def exec(self):
        db_name, col_name, query = Collection.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        query_object = parser.hyperql_parser(query)
        acknowledgement = {
            "Ack": col.update(query_object, self.data.user_data),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class DeleteProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data

    def exec(self):
        db_name, col_name, object_id = Collection.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.delete(object_id),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class ReadOneProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data

    def exec(self):
        db_name, col_name, query = BaseRIDUProcess.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        query_object = parser.hyperql_parser(query)
        return {
            "Ack": col.readOne(query_object),
            "addr": self.data.addr
        }


class UpdateOneProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data

    def exec(self):
        db_name, col_name, object_id = Collection.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.updateOne(object_id, self.data.user_data),
            "addr": self.data.addr
        }

        Event.emmit('col-change', col)
        return acknowledgement


class ReadByIdProcess(Process):
    def __init__(self, parsed_data):
        self.data = parsed_data

    def exec(self):
        db_name, col_name, object_id = Collection.meta_separator(self.data.meta_data)
        col = Collections.get_collection(col_name, db_name)
        acknowledgement = {
            "Ack": col.findById(object_id),
            "addr": self.data.addr
        }
        return acknowledgement



def renderRIDUProcess(parsed_data):
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
