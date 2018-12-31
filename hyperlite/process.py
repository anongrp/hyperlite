""" Its all about processes and tasks  """

from enum import Enum

class ProcessType(Enum):
    Query = 1
    Writing = 2


class Process:
    def __init__(self):
        self.type: ProcessType

    def exec(self):
        pass