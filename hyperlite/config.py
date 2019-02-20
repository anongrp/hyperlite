""" Contain All The Configurations & Settings """

import os, sys

# Hold the current running platform
PLATFORM = "Windows" if sys.platform.lower().find("win") > -1 else "Linux"


# *Private* Path for database if platform is windows
_WIN_DB_PATH = r"C:\\data\\hyperlite_db"

# *Private* Path for database if platform is linux
_LINUX_DB_PATH = r"/home/.data/hyperlite_db"

# *Public* it's used in production
DATABASE_PATH = _WIN_DB_PATH if PLATFORM == "Windows" else _LINUX_DB_PATH

# Database format
DATABASE_FORMAT = {
    'type': 'bson',
    'format': 'binary'
}

DEFAULT = {
    "port": 9898,
    "host": "localhost"
}