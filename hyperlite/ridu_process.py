"""   It's all about processes and tasks. """

import json

from .request_parser import ParsedData
from .collection import Collection
from .collection import Collections
from .database import Databases
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

            # Retrieve db_name, col_name and HyperQL query
            # from the process_data
            db_name, col_name, query = Collection.meta_separator(self.process_data.meta_data)

            # get Collection object
            # on which operation is to be performed
            col = Collections.get_collection(col_name, db_name)

            # get Query() object from HyperQL query
            # Query() contains required_field and needed_query_methods
            query_object = parser.hyperql_parser(query)
            
            if self.process_data.request_type == 'Read':

                return {
                    "Ack": col.read(query_object),
                    "addr": self.process_data.addr
                }
            
            else:

                acknowledgement = {
                    "Ack": col.update(query_object),
                    "addr": self.process_data.addr
                }

            Event.emmit('col-change', col)
            return acknowledgement
            
        # If the RequestType is Insert
        elif self.process_data.request_type == 'Insert':

            # Retrieve db_name, col_name from the process_data
            db_name, col_name = Collection.meta_separator(self.process_data.meta_data)

            # get Collection object
            # on which operation is to be performed
            col = Collections.get_collection(col_name, db_name)

            # Insert user_data as new Object in specified Collection
            # and return object id as acknowledgement.
            acknowledgement = {
                "Ack": col.insert(self.process_data.user_data),
                "addr": self.process_data.addr
            }

            Event.emmit('col-change', col)
            return acknowledgement

        # If the RequestType is Delete
        elif self.process_data.request_type == 'Delete':

            # Retrieve db_name, col_name and object_id from the process_data
            db_name, col_name, object_id = Collection.meta_separator(self.process_data.meta_data)

            # get Collection object
            # on which operation is to be performed
            col = Collections.get_collection(col_name, db_name)

            acknowledgement = {
                "Ack": col.delete(object_id),
                "addr": self.process_data.addr
            }

            Event.emmit('col-change', col)
            return acknowledgement

        raise Exception
