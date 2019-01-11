"""   Contains Information of the Collection   """

from .database import Database


class Collection:

    def __init__(self, col_name: str, parent: Database):
        self.col_name = col_name
        self.objects = []
        self.indices = {}
        self.parent = parent
        Collections.add_collection(self)

    def __str__(self):
        return self.col_name

    def insert(self, user_data: dict):
        object_id = Objects.generate_id(self)
        self.objects.append(user_data)
        self.indices.update({
            object_id: self.objects.__len__()
        })
        return object_id

    def update(self, *args, **kwargs):
        pass

    def read(self, objects: list, instruction: dict = {}, instructions: list = []):
        output_objs =[]
        if not instructions:
            for object in objects:
                print(instruction['filter'](data=instruction['data'], field=object[instruction['field']]))
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
