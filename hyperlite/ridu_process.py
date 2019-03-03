"""   It's all about processes and tasks. """

from .request_parser import ParsedData
from .collection import Collection
from .collection import Collections
from hyperql import parser
from hyperlite.event import Event


class Process(object):
    """     
        This class creates an executable process for every task.    

        Takes ParsedData() as parameter and executes the operations
        on ParsedData() as per it's Request Type.
    """

    def __init__(self, process_data: ParsedData):
        self.process_data: ParsedData = process_data

    def exec(self):
        """
            Instance method to execute Process().

            exec method executes the task associated with the Process.
            It resolves the tasks on the basis of the RequestType of the ParsedData().
        """

        # If the RequestType is Read or Update
        if self.process_data.request_type == 'Read' or self.process_data.request_type == 'Update':

            db_name, col_name, query = Collection.meta_separator(self.process_data.meta_data)

            col = Collections.get_collection(col_name, db_name)

            query_object = parser.hyperql_parser(query)
            
            if self.process_data.request_type == 'Read':

                    return {
                        "Ack": col.read(query_object),
                        "addr": self.process_data.addr
                    }
            
            else:

                acknowledgement = {
                    "Ack": col.update(query_object, self.process_data.user_data),
                    "addr": self.process_data.addr
                }

            Event.emmit('col-change', col)
            return acknowledgement
            
        # If the RequestType is Insert
        elif self.process_data.request_type == 'Insert':

            db_name, col_name = Collection.meta_separator(self.process_data.meta_data)

            col = Collections.get_collection(col_name, db_name)

            acknowledgement = {
                "Ack": col.insert(self.process_data.user_data),
                "addr": self.process_data.addr
            }

            Event.emmit('col-change', col)
            return acknowledgement

        # If the RequestType is Delete
        elif self.process_data.request_type == 'Delete':

            db_name, col_name, object_id = Collection.meta_separator(self.process_data.meta_data)

            col = Collections.get_collection(col_name, db_name)

            acknowledgement = {
                "Ack": col.delete(object_id),
                "addr": self.process_data.addr
            }

            Event.emmit('col-change', col)
            return acknowledgement

        raise Exception