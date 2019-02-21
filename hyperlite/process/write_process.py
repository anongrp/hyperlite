from storage_engine import coliter


class WriteProcess(object):
    def __init__(self, collection):
        self.collection = collection

    def exec(self):
        coliter.writer(self.collection)


def rendererProcess(collection):
    return WriteProcess(collection)
