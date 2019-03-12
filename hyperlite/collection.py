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

import uuid
import copy

from hyperql import parser
from .logger import Log

DEFAULT_QUERY = parser.Query()
TAG = "Collection_API"


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

        object_id = uuid.uuid4().hex  # unique id for every object
        user_data['_id'] = object_id
        self.objects.append(user_data)  # append new object to objects list

        self.indexes.update({
            object_id: self.objects.__len__() - 1
        })
        return object_id

    def insertAll(self, user_data: list):
        """
        InsertAll operations: Useful for Inserting a list of objects together.
        :param user_data: list of data to be inserted
        :return: objects_id: list of _id of inserted objects
        """
        Log.d(TAG, type(user_data))
        Log.d(TAG, type(user_data[0]))
        objects_id = []
        if type(user_data) is list:
            Log.d(TAG, "Type list")
            for data in user_data:
                if type(data) is dict:
                    Log.d(TAG, "Type dict")
                    objects_id.append(self.insert(data))
        Log.d(TAG, f"{objects_id}")
        return objects_id

    def _update(self, new_data: dict, update_objects: list):
        """     Private method to update an object of the collection.    """

        for hy_object in update_objects:
            for prop in new_data:
                if type(new_data[prop]) is dict:
                    prop1 = list(new_data[prop].keys())[0]
                    operator = list(new_data[prop][prop1].keys())[0]
                    if operator == "&inc":
                        try:
                            hy_object[prop] += new_data[prop][prop1][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] += new_data[prop][prop1][operator]

                    if operator == "&dec":
                        try:
                            hy_object[prop] -= new_data[prop][prop1][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] -= new_data[prop][prop1][operator]

                    if operator == "&mul":
                        try:
                            hy_object[prop] *= new_data[prop][prop1][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] *= new_data[prop][prop1][operator]

                    if operator == "&div":
                        try:
                            hy_object[prop] /= new_data[prop][prop1][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] /= new_data[prop][prop1][operator]

                    if operator == "&pow":
                        try:
                            hy_object[prop] **= new_data[prop][prop1][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] **= new_data[prop][prop1][operator]

                    if operator == "&floor":
                        try:
                            hy_object[prop] //= new_data[prop][prop1][operator]
                        except KeyError:
                            hy_object[prop] = 0
                            hy_object[prop] //= new_data[prop][prop1][operator]

                else:
                    hy_object[prop] = new_data[prop]
        return True

    def updateAll(self, query_object: parser.Query, new_data):
        """
            Instance method to update Object's data of Collection.
            Takes query_object and new_data: dict as parameter and returns bool value.
        """

        filtered_data = None

        for instruction in query_object.selective:

            if filtered_data is None:
                filtered_data = self.execSelectiveQuery(objects=self.objects, instruction=instruction)
            else:
                filtered_data = self.execSelectiveQuery(objects=filtered_data, instruction=instruction)

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

    def execSelectiveQuery(self, objects: list, instruction):
        output_objs = []

        for hy_object in objects:
            if instruction['field'].find('.') == -1:
                if instruction['field'] in hy_object and instruction['filter'](data=instruction['data'],
                                                                               field=hy_object[
                                                                                   instruction['field']]):
                    output_objs.append(hy_object)
            else:
                currentObj = hy_object
                for field in instruction['field'].split('.'):
                    if field in currentObj:
                        currentObj = currentObj[field]
                        if instruction['filter'](data=instruction['data'], field=currentObj):
                            output_objs.append(hy_object)
                            break
        return output_objs

    def _read(self, objects: list, instruction, view, modifiers):
        """     Private method to read the Objects data from the collection.    """

        output_objs = []

        for hy_object in objects:
            isNeeded = False
            if instruction['field'].find('.') == -1:
                if instruction['field'] in hy_object and instruction['filter'](data=instruction['data'],
                                                                               field=hy_object[
                                                                                   instruction['field']]):
                    # output_objs.append(hy_object)
                    isNeeded = True
            else:
                currentObj = hy_object
                for field in instruction['field'].split('.'):
                    if field in currentObj:
                        currentObj = currentObj[field]
                        if instruction['filter'](data=instruction['data'], field=currentObj):
                            # output_objs.append(hy_object)
                            isNeeded = True
                            break
            if isNeeded:
                if type(view) is list:
                    output_obj = {}
                    for instruction in view:
                        currentObj = hy_object
                        for instruct in instruction.split('.'):
                            if instruct in currentObj:
                                currentObj = currentObj[instruct]
                            else:
                                currentObj = None
                        output_obj[instruction] = currentObj
                    output_objs.append(output_obj)
                else:
                    output_objs.append(hy_object)
        if modifiers != DEFAULT_QUERY.modifiers:
            if modifiers is not None:
                output_objs = output_objs[modifiers['skip']:modifiers['skip'] + modifiers['limit']]

        return output_objs

    def read(self, query_object: parser.Query, one_flag=False):
        """
            Instance method to get Object's data from Collection.
            Takes query_object as parameter and returns a list of Hyperlite Objects.
            The HyperQl query is parsed with bottom-up approach,
            filtered_data stores the remaining data after every iteration of
            query parsing.
        """

        if one_flag is True:
            query_object.modifiers['limit'] = 1
            filtered_data = self._read(self.objects, query_object.selective, query_object.view, query_object.modifiers)
            if not filtered_data:
                return filtered_data
            else:
                return filtered_data[0]
        else:
            return self._read(self.objects, query_object.selective, query_object.view, query_object.modifiers)

    def delete(self, object_id: str) -> bool:
        """
            Instance method to remove object.
            takes object_id as parameter.
        """
        if self.findById(object_id) is not None:
            self.objects[self.indexes[object_id]] = None
            self.indexes[object_id] = None
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
