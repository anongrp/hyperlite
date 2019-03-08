import logging
import os
from termcolor import colored
from hyperlite.config import *

os.makedirs(LOG_DIRECTORY) if not os.path.exists(LOG_DIRECTORY) else print()
logging.basicConfig(filename=GLOBAL_LOG_FILE_PATH,
                    format='%(message)s',
                    filemode='w')


"""
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
"""


class Log:
    """ Class for logging data into console and file to debug """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    @staticmethod
    def d(tag, message):
        """
        for debugging purpose only
        :param tag: to categorize from other debug statement
        :param message: to print on console
        :return: :None
        """
        level = "Debug:"
        message = f"{tag:20}{level:10}{message}"
        print(colored(message, 'white', attrs=['bold']))
        Log.logger.debug(message)

    @staticmethod
    def i(tag, message):
        """
        to show information about location or event execution
        :param tag: to categorize from other debug statement
        :param message: to print on console
        :return: :None
        """
        level = "Info:"
        message = f"{tag:20}{level:10}{message}"
        print(colored(message, 'blue'))
        Log.logger.info(message)

    @staticmethod
    def e(tag, message):
        """
        to show error on console or in log file
        :param tag: to categorize from other debug statement
        :param message: to print on console
        :return: :None
        """
        level = "Error:"
        message = f"{tag:20}{level:10}{message}"
        print(colored(message, 'red'))
        Log.logger.error(message)

    @staticmethod
    def w(tag, message):
        """
        to show warning like unable to write on disk etc.
        :param tag: to categorize from other debug statement
        :param message: to print on console
        :return: :None
        """
        level = "Warning:"
        message = f"{tag:20}{level:10}{message}"
        print(colored(message, 'yellow'))
        Log.logger.warning(message)

    @staticmethod
    def c(tag, message):
        """
        to show critical messages like 'writing collection on disk takes too long time etc'
        :param tag: to categorize from other debug statement
        :param message: to print on console
        :return: :None
        """
        level = "Critical:"
        message = f"{tag:20}{level:10}{message}"
        print(colored(message, 'red', attrs=['bold']))
        Log.logger.critical(message)


# TAG = __file__.split('/')[len(__file__.split('/')) - 1]
# Log.d(TAG, "Its a debug , just for test")
# Log.i(TAG, "Ack delivered to client")
# Log.e(TAG, "Its a error in collection class, File not found")
# Log.w(TAG, "Its a warning program takes too much of time to write file on disk")
# Log.c(TAG, "its a critical part its not good for speed")
