"""   Contains Information about the Collections.

    --------------------
    Classes :
        
        -----------------
        * Collection

        * Collections

        * Objects
        -----------------

    --------------------
"""

import time
from hyperlite.event import Event
from hyperql import parser

DEFAULT_QUERY = parser.Query()


class Collection:
    """
        This class refers to the Collection itself.
        
        A Collection is a group of hyperlite objects ( similar to RDBMS table ).

        Every Collection is represented by an object of Collection class.
    """

    def __init__(self, col_name: str, parent: str):
        """
            Every collection contains a name, list of objects,
            indices and parent db object.
        """
        self.col_name = col_name
        self.objects = []
        self.indices = {}  # indices is a dict object
        # which stores object id as key
        # and object index as value

        self.parent = parent
        Collections.add_collection(self)  # Adds the collection to existing group of col.

    def __str__(self):
        """     String representation of collection.    """
        return str(self.__dict__)

    def insert(self, user_data: dict):
        """ 
            Instance method to insert new object into collection.

            Takes user data as parameter.
        """

        object_id = Objects.generate_id(self)  # unique id for every object

        self.objects.append(user_data)  # append new object to objects list

        # update indices dict for new object
        self.indices.update({
            object_id: self.objects.__len__() - 1
        })

        return object_id

    def _update(self, new_data: dict, update_objects: list):
        """     Private method to update an object of the collection.    """

        for hy_object in update_objects:
            for prop in new_data:
                if type(new_data[prop]) is dict:
                    operator = list(new_data[prop].keys())[0]
                    if operator == "&inc":
                        try:
                            hy_object[prop] += new_data[prop][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] += new_data[prop][operator]

                    if operator == "&dec":
                        try:
                            hy_object[prop] -= new_data[prop][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] -= new_data[prop][operator]

                    if operator == "&mul":
                        try:
                            hy_object[prop] *= new_data[prop][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] *= new_data[prop][operator]

                    if operator == "&div":
                        try:
                            hy_object[prop] /= new_data[prop][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] /= new_data[prop][operator]

                    if operator == "&pow":
                        try:
                            hy_object[prop] **= new_data[prop][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] **= new_data[prop][operator]

                    if operator == "&floor":
                        try:
                            hy_object[prop] //= new_data[prop][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] //= new_data[prop][operator]

                else:
                    hy_object[prop] = new_data[prop]
            print()
            print()
            print(hy_object)
            print()
            print()
        return True

    def updateAll(self, query_object, new_data):
        """
            Instance method to update Object's data of Collection.

            Takes query_object and new_data: dict as parameter and returns bool value.
        """
        filtered_data = None

        for instruction in query_object.needed_query_methods:

            # For first iteration
            if filtered_data is None:
                filtered_data = self._read(objects=self.objects, instruction=instruction)
            # If filtered_data is not None
            else:
                filtered_data = self._read(objects=filtered_data, instruction=instruction)

        return self._update(new_data=new_data, update_objects=filtered_data)

    def updateOne(self, object_id: str, new_data: dict):
        """
            Instance method to update a single Object data of Collection.

            Takes object_id and new_data: dict as parameter and returns bool value.
        """
        update_obj = self.findById(object_id)

        if update_obj is not None:
            return self._update(new_data, [update_obj])
        else:
            return False

    def _read(self, objects: list, instruction: dict = {}, instructions: list = [], modifiers=None):
        """     Private method to read the Objects data from the collection.    """

        output_objs = []
        if not instructions:
            for object in objects:
                if instruction['filter'](data=instruction['data'], field=object[instruction['field']]):
                    output_objs.append(object)
        else:
            for object in objects:
                output_obj = {}
                for instruction in instructions:
                    if object[instruction['field']]:
                        output_obj.update({
                            instruction['field']: object[instruction['field']]
                        })
                output_objs.append(output_obj)

        if modifiers != DEFAULT_QUERY.modifiers:
            if modifiers is not None:
                output_objs = output_objs[modifiers['skip']:modifiers['skip'] + modifiers['limit']]

        return output_objs

    def read(self, query_object, one_flag=False):
        """
            Instance method to get Object's data from Collection.

            Takes query_object as parameter and returns a list of Hyperlite Objects.

            The HyperQl query is parsed with bottom-up approach,
            filtered_data stores the remaining data after every iteration of
            query parsing.
        """
        filtered_data = None
        echo_queries = []  # stores echo query instructions

        for instruction in query_object.needed_query_methods[::-1]:
            if instruction['filter'] is not parser.QueryOperations.echo:

                # For first iteration
                if filtered_data is None:
                    filtered_data = self._read(objects=self.objects, instruction=instruction)
                # If filtered_data is not None
                else:
                    filtered_data = self._read(objects=filtered_data, instruction=instruction)
            else:
                echo_queries.append(instruction)

        if one_flag is True:
            return self._read(objects=[filtered_data[0]], instructions=echo_queries, modifiers=query_object.modifiers)

        # Perform all echo operations together and return required data.
        return self._read(objects=filtered_data, instructions=echo_queries, modifiers=query_object.modifiers)

    def delete(self, object_id: str) -> bool:
        """
            Instance method to remove object.

            takes object_id as parameter.
        """
        if self.findById(object_id) is not None:

            self.indices[self.findById(object_id)] = None
            return True
        else:
            return False

    def findById(self, object_id: str):
        """
            Private Instance method to get object from object id.
            returns object associated with the given object_id.
        """
        try:
            return self.indices[object_id]

        except KeyError:
            # if object_id is not available
            return None

    def readOne(self, query_object):
        """
            Instance method to get first Object's data from Collection.

            Takes query_object as parameter and returns first encountered Hyperlite Object.
        """
        return self.read(query_object, one_flag=True)

    @classmethod
    def meta_separator(cls, meta_data: dict) -> list:
        """
            @classmethod to fetch meta data from dict.

            if meta_data is of Read RequestType,
            then returns list containing db_name, col_name and Query

            if meta_data is of Insert RequestType,
            then returns list containing db_name and col_name.

            if meta_data is of Delete RequestType,
            then returns list containing db_name, col_name and object_id.

            if meta_data is of Update RequestType,
            then returns list containing db_name, col_name and object_id.

        """
        return [meta for meta in meta_data.values()]


class Collections:
    """   Maintains record of all Collections   """
    collection_list = {}
    meta_collection: Collection = None

    """
    {
        database: {  // set of collection
            collection,
            collection,
            collection,
            collection
        },
        another_database: {  // set of collection
            collection,
            collection,
            collection,
            collection
        },
    }
    """

    @classmethod
    def add_collection(cls, collection: Collection):
        if Collections.collection_list.get(collection.parent) is not None:
            Collections.collection_list.get(collection.parent).add(collection)
        else:
            Collections.collection_list.update({
                collection.parent: {collection}
            })

    @classmethod
    def get_collection(cls, col_name: str, db_name):
        if Collections.collection_list.get(db_name) is not None:
            database = Collections.collection_list.get(db_name)
            for collection in database:
                if col_name == collection.col_name:
                    return collection
                else:
                    # Fetching or create new Collection
                    new_collection = Collection(col_name, db_name)
                    Collections.add_collection(new_collection)
                    Collections.meta_collection.insert({
                        "db_name": db_name,
                        "col_name": col_name,
                        "time_stamp": parserTimeStamp(str(time.time())),  # its helps to find this collection on disk
                        "user": "Anonymous"
                    })
                    Event.emmit('col-change', Collections.meta_collection)
                    return new_collection
        else:
            new_collection = Collection(col_name, db_name)
            Collections.add_collection(new_collection)
            Collections.meta_collection.insert({
                "db_name": db_name,
                "col_name": col_name,
                "time_stamp": parserTimeStamp(str(time.time())),  # its helps to find this collection on disk
                "user": "Anonymous"
            })
            Event.emmit('col-change', Collections.meta_collection)
            return new_collection


def parserTimeStamp(time_stamp):
    return time_stamp[0: time_stamp.find('.')]

class Objects:
    """ Helps to Maintain record of all Objects """
    object_count = 0

    @classmethod
    def generate_id(cls, collection: Collection) -> str:
        obj_id = collection.parent + '.' + collection.col_name + '.' + str(Objects.object_count + 1)
        return obj_id
