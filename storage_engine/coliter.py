import _pickle
from hyperlite import config
from hyperlite.collection import Collection

import os
import time
from hyperlite import collection


def writer(collection: Collection):
    try:
        print(collection)
        doctor()
        _pickle.dump(collection, open(__getNewCollectionUri(), "wb"))
        print("Saved to disk")
        return True
    except Exception as ex:
        print("Error in collection writer")
        return False
    
    
def reader(collectionName: str):        #give it name of .col file, it will read it from disk and return collection object
        try:
            if not '.' + config.DATABASE_FORMAT["type"]  in collectionName:         #if there's no .col in name, add it
                collectionName = collectionName + '.' + config.DATABASE_FORMAT["type"] 
                
            filePath = config.DATABASE_PATH + __getPathSeparator() + collectionName

            with open(filePath, 'rb') as f:
                collection = _pickle.load(f)        #loading the collection object
        
            return collection           #returning collection object

        except Exception as e:
            print("Some error occured")


def doctor():
    if not os.path.exists(config.DATABASE_PATH):
        os.makedirs(config.DATABASE_PATH)   # mkdir() for just one folder, makedirs() for creating multiple nested folders
        
        
def listCollectionOnDisk():                             #a list having name of all .col files on the disk
        allfiles = os.listdir(config.DATABASE_PATH)     #getting all files in our database path
        collectionFiles = filterFiles(allfiles)         #getting only .col files from there
        return collectionFiles                          #returning list of all .col files present in our DB


def filterFiles(unfilteredfiles: list):         #in listdir, we get all types of files and folders, 
        filtered = []                           #we need only collection files
        for i in unfilteredfiles:
            if '.' + config.DATABASE_FORMAT["type"] in i:
                filtered.append(i)
        return filtered


def __getNewCollectionUri() -> str:
    return config.DATABASE_PATH + __getPathSeparator() + __generateColFileName()


def __generateColFileName() -> str:
    name = str(time.time())
    return name[0: name.find('.')] + name[name.find('.'): len(name)] + "." + config.DATABASE_FORMAT["type"]


def __getPathSeparator() -> str:
    return "/" if config.PLATFORM == "Linux" else r"\\"
