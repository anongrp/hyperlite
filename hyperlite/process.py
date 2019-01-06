""" Its all about processes and tasks  """

from .request_parser import ParsedData
from .collection import Collection
from .collection import Collections
from .database import Databases


class Process:
    def __init__(self, process_data: ParsedData):
        self.process_data: dict = process_data

    def exec(self):
        if self.process_data.request_type == 'Read':
            pass
        elif self.process_data.request_type == 'Insert':
            db_name, col_name = Collection.meta_separator(self.process_data.meta_data)
            db = Databases.get_db(db_name)
            col = Collections.get_collection(col_name)
            if col.parent is db:
                col.insert(self.process_data.user_data)
                print('Yup, It works...')
        elif self.process_data.request_type == 'Delete':
            pass
        elif self.process_data.request_type == 'Update':
            pass
        else:
            pass
