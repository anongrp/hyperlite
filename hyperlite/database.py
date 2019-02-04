"""   Contains Information about the Databases.

    --------------------
    Classes :
        
        -----------------
        * Database

        * Databases
        -----------------

    --------------------
"""

from time import gmtime, strftime


class Database(object):
    """
        This class refers to the database itself.
        
        Every Database is represented by an object of Database class.
    """
    def __init__(self, db_name: str):
        """
            Every database contains a name and creation date and time.
        """
        self.db_name = db_name
        self.creation_date: str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        Databases.add_db(self)  # Adds the database to existing group of db.

    def __str__(self):
        """     String representation of database.    """
        return self.db_name + '\n' + str(self.creation_date)


class Databases(object):
    """    Maintains record of all open Databases.    """

    # db_list is a dict object which contains
    # database name as key 
    # and Database object as value
    db_list = {}

    @classmethod
    def add_db(cls, db: Database):
        """    @classmethod to add new database to existing group of db.    """

        Databases.db_list.update({
            db.db_name: db
        })

    @classmethod
    def get_db(cls, db_name: str):
        """    @classmethod to retrieve Database object by passing db_name as parameter    """

        return Databases.db_list.get(db_name)
