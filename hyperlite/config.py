""" Contain All The Configurations & Settings """

import getpass
import sys


def __getPathSeparator() -> str:
    return "/" if PLATFORM == "Linux" else r"\\"


# Hold the current running platform
PLATFORM = "Windows" if sys.platform.lower().find("win") > -1 else "Linux"

# *Private* Path for database if platform is windows
_WIN_DB_PATH = r"C:\\data\\hyperlite"

# *Private* Path for database if platform is linux
_LINUX_DB_PATH = r"/home/" + getpass.getuser() + "/.data/hyperlite"

# *Public* it's used in production
DATABASE_PATH = _WIN_DB_PATH if PLATFORM == "Windows" else _LINUX_DB_PATH

DEFAULT_META_COLLECTION_NAME = "hyperlite.col"
COLLECTION_PATH = DATABASE_PATH + __getPathSeparator() + DEFAULT_META_COLLECTION_NAME

# Database format
DATABASE_FORMAT = {
    'type': 'col',
    'format': 'binary'
}

DEFAULT = {
    "port": 8989,
    "host": "127.0.0.1"
}

LOG_DIRECTORY = DATABASE_PATH + __getPathSeparator() + "Log"
GLOBAL_LOG_FILE_PATH = LOG_DIRECTORY + __getPathSeparator() + "global.log"
