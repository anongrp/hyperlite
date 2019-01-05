""" Its all about processes and tasks  """

from enum import Enum

class Process:
    def __init__(self, process_name: ProcessType, process_data: dict):
        self.process_name: ProcessType = process_name
        self.process_data: dict = process_data

    def exec(self):
        pass