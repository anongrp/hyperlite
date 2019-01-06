"""   Contains Information of the Database   """

from time import gmtime, strftime


class Database:

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.creation_date: str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        Databases.add_db(self)

    def __str__(self):
        return self.db_name + '\n' + str(self.creation_date)


class Databases:
    """   Maintains record of all open Databases   """
    db_list = {}

    @classmethod
    def add_db(cls, db: Database):
        Databases.db_list.update({
            db.db_name: db
        })

    @classmethod
    def get_db(cls, db_name: str):
        return Databases.db_list.get(db_name)
