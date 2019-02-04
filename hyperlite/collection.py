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

from .database import Database


class Collection:
    """
        This class refers to the Collection itself.
        
        A Collection is a group of hyperlite objects ( similar to RDBMS table ).

        Every Collection is represented by an object of Collection class.
    """

    def __init__(self, col_name: str, parent: Database):
        """
            Every collection contains a name, list of objects,
            indices and parent db object.
        """
        self.col_name = col_name
        self.objects = []
        self.indices = {}        # indices is a dict object
        # which stores object id as key
        # and object index as value

        self.parent = parent
        Collections.add_collection(self)    # Adds the collection to existing group of col.

    def __str__(self):
        """     String representation of collection.    """
        return self.col_name

    def insert(self, user_data: dict):
        """ 
            Instance method to insert new object into collection.

            Takes user data as parameter.
        """

        object_id = Objects.generate_id(self) # unique id for every object

        self.objects.append(user_data) # append new object to objects list

        # update indices dict for new object
        self.indices.update({
            object_id: self.objects.__len__() - 1
        })

        return object_id

    def update(self, *args, **kwargs):
        """     Instance method to update an object of the collection.    """

        # underdevelopment

        pass

    def read(self, objects: list, instruction: dict = {}, instructions: list = []):
        output_objs =[]
        if not instructions:
            for object in objects:
                if instruction['filter'](data=instruction['data'], field=object[instruction['field']]):
                    output_objs.append(object)
            return output_objs
        else:
            for object in objects:
                output_obj = {}
                for instruction in instructions:
                    if object[instruction['field']]:
                        output_obj.update({
                            instruction['field']: object[instruction['field']]
                        })
                output_objs.append(output_obj)
        return output_objs

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def meta_separator(cls, meta_data: dict) -> list:
        return [meta for meta in meta_data.values()]


class Collections:
    """   Maintains record of all Collections   """
    collection_list = {}

    @classmethod
    def add_collection(cls, collection: Collection):
        Collections.collection_list.update({
            collection.col_name: collection
        })

    @classmethod
    def get_collection(cls, col_name: str):
        collection = Collections.collection_list.get(col_name)
        return collection


class Objects:
    """    Helps to Maintain record of all Objects"""
    object_count = 0

    @classmethod
    def generate_id(cls, collection: Collection) -> str:
        obj_id = collection.parent.db_name + '.' + collection.col_name + '.' + str(Objects.object_count + 1)
        return obj_id
