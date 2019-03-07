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
import uuid
from hyperlite.event import Event
from hyperql import parser
from storage_engine import initializer
from hyperlite import config

DEFAULT_QUERY = parser.Query()


class Collection:

    def __init__(self, col_name: str, parent: str):
        """
        :param col_name: name of the collection, which is unique for in every database
        :param parent: parent is a database name, where this collection is belong to
        """
        self.col_name = col_name
        self.objects = []
        self.indexes = {}
        self.parent = parent

    def __str__(self):
        return str(self.__dict__)

    def insert(self, user_data: dict):
        """
        Insert operation: One of the most important op in RIDU's Operations
        :param user_data: it's a type of dictionary
        :return: objectId: it's a type of string
        """
        object_id = Objects.generate_id()  # unique id for every object
        user_data['_id'] = object_id
        self.objects.append(user_data)  # append new object to objects list

        self.indexes.update({
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

    def _read(self, objects: list, instruction={}, instructions=[], modifiers=None):
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
                else:
                    filtered_data = self._read(objects=filtered_data, instruction=instruction)
            else:
                echo_queries.append(instruction)

        if one_flag is True:
            if not filtered_data:
                return filtered_data
            else:
                return self._read(objects=[filtered_data[0]], instructions=echo_queries, modifiers=query_object.modifiers)
        # Perform all echo operations together and return required data.
        return self._read(objects=filtered_data, instructions=echo_queries, modifiers=query_object.modifiers)

    def delete(self, object_id: str) -> bool:
        """
            Instance method to remove object.
            takes object_id as parameter.
        """
        if self.findById(object_id) is not None:
            self.indexes[self.findById(object_id)] = None
            return True
        else:
            return False

    def findById(self, object_id: str):
        """
            Private Instance method to get object from object id.
            returns object associated with the given object_id.
        """
        try:
            return self.objects[self.indexes[object_id]]

        except KeyError:
            # if object_id is not available
            return None

    def readOne(self, query_object):
        """
        Instance method to get first Object from Collection.
        :param query_object: object of Query class `from hyperql.parser import Query`
        :return: result after applying the query
        """

        return self.read(query_object, one_flag=True)

    @classmethod
    def meta_separator(cls, meta_data: dict) -> list:
        """
            @classmethod to fetch meta data from dict.

            if meta_data is of Read RequestType, then returns list containing db_name, col_name and Query
            if meta_data is of Insert RequestType, then returns list containing db_name and col_name.
            if meta_data is of Delete RequestType, then returns list containing db_name, col_name and object_id.
            if meta_data is of Update RequestType, then returns list containing db_name, col_name and object_id.
        """
        return [meta for meta in meta_data.values()]


class Collections:
    """   Maintains record of all Collections   """
    collection_list = {}
    meta_collection: Collection = None

    @classmethod
    def create_new_collection(cls, col_name, db_name):
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
                        time_stamp = it,
                        db_name &eq "{db_name}",
                        col_name &eq "{col_name}"
                        """
                result = Collections.meta_collection.readOne(parser.hyperql_parser(query))
                if not result:
                    print("Getting new collection because collection is not in ram and also on a disk")
                    return Collections.create_new_collection(col_name, db_name)
                else:
                    result = result[0]
                    print("Getting collection from disk")
                    result = initializer.getCollection(
                        config.DATABASE_PATH + getPathSeparator() + str(result.get("time_stamp")) + ".col")
                    Collections.add_collection(result)
                    return result
        else:
            query = """
                    time_stamp = it,
                    db_name &eq "{}",
                    col_name &eq "{}"
                    """.format(db_name, col_name)
            result = Collections.meta_collection.readOne(parser.hyperql_parser(query))
            if not result:
                print("Getting new collection: @no database found")
                return Collections.create_new_collection(col_name, db_name)
            else:
                result = result[0]
                print("Getting collection from disk: @root else")
                result = initializer.getCollection(
                    config.DATABASE_PATH + getPathSeparator() + str(result.get('time_stamp')) + ".col")
                Collections.add_collection(result)
                return result


def parserTimeStamp(time_stamp):
    return time_stamp[0: time_stamp.find('.')]


def getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"


class Objects:
    """ Helps to Maintain record of all Objects """
    object_count = 0

    @classmethod
    def generate_id(cls) -> str:
        obj_id = uuid.uuid4()
        return str(obj_id.hex)
