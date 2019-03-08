import logging
import os
from termcolor import colored
from hyperlite.config import *

os.makedirs(LOG_DIRECTORY) if not os.path.exists(LOG_DIRECTORY) else print()
logging.basicConfig(filename=GLOBAL_LOG_FILE_PATH,
                    format='%(levelname)s: '
                           '%(message)s',
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
    def d(message):
        """
        for debugging purpose only
        :param message: to print on console
        :return: :None
        """
        print(colored(f"Debug: {message}", 'white', attrs=['bold']))
        Log.logger.debug(message)

    @staticmethod
    def i(message):
        """
        to show information about location or event execution
        :param message: to print on console
        :return: :None
        """
        print(colored(f"Info: {message}", 'blue'))
        Log.logger.info(message)

    @staticmethod
    def e(message):
        """
        to show error on console or in log file
        :param message: to print on console
        :return: :None
        """
        print(colored(f"Error: {message}", 'red'))
        Log.logger.error(message)

    @staticmethod
    def w(message):
        """
        to show warning like unable to write on disk etc.
        :param message: to print on console
        :return: :None
        """
        print(colored(f"Warning: {message}", 'yellow', attrs=['underline']))
        Log.logger.warning(message)

    @staticmethod
    def c(message):
        """
        to show critical messages like 'writing collection on disk takes too long time etc'
        :param message: to print on console
        :return: :None
        """
        print(colored(f"Critical: {message}", 'red', attrs=['underline', 'bold']))
        Log.logger.critical(message)


# Log.d("Its a debug , just for test")
# Log.i("Ack delivered to client")
# Log.e("Its a error in collection class, File not found")
# Log.w("Its a warning program takes too much of time to write file on disk")
# Log.c("its a critical part its not good for speed")
