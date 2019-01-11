""" Its all about processes and tasks  """

from .request_parser import ParsedData
from .collection import Collection
from .collection import Collections
from .database import Databases
from hyperql import parser


class Process:
    def __init__(self, process_data: ParsedData):
        self.process_data: dict = process_data

    def exec(self):
        if self.process_data.request_type == 'Read':
            db_name, col_name, query = Collection.meta_separator(self.process_data.meta_data)
            db = Databases.get_db(db_name)
            col = Collections.get_collection(col_name)
            query_object = parser.hyperql_parser(query)
            echo_queries = []
            if col.parent is db:
                filtered_data = None
                for instruction in query_object.needed_query_methods[::-1]:
                    if instruction['filter'] is not parser.QueryOperations.echo:
                        if filtered_data is None:
                            filtered_data = col.read(objects=col.objects, instruction=instruction)
                        else:
                            filtered_data = col.read(objects=filtered_data, instruction=instruction)
                    else:
                        echo_queries.append(instruction)
                return col.read(objects=filtered_data, instructions=echo_queries)
        elif self.process_data.request_type == 'Insert':
            db_name, col_name = Collection.meta_separator(self.process_data.meta_data)
            db = Databases.get_db(db_name)
            col = Collections.get_collection(col_name)
            if col.parent is db:
                return col.insert(self.process_data.user_data)
        elif self.process_data.request_type == 'Delete':
            pass
        elif self.process_data.request_type == 'Update':
            pass
        else:
            pass
