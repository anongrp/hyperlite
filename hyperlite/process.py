""" Its all about processes and tasks  """

from enum import Enum


class ProcessType(Enum):
    Read = 1
    Insert = 2
    Delete = 3
    Update = 4


class Process:
    def __init__(self, process_name: ProcessType, process_data: dict):
        self.process_name: ProcessType = process_name
        self.process_data: dict = process_data

    def exec(self):
        pass
