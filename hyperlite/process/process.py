from storage_engine import coliter
from ..collection import Collection


class Process(object):
    def exec(self):
        pass


class WriteProcess(Process):
    def __init__(self, collection: Collection):
        self.collection = collection

    def exec(self) -> bool:
        return coliter.postWriter(self.collection)


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


def renderProcess(collection: Collection):
    process = []
    # if _shouldDefrag():
    #     process.append(DefragProcess(collection))
    # process.append(EncryptionProcess(collection))
    process.append(WriteProcess(collection))
    return process


def _shouldDefrag() -> bool:
    pass
