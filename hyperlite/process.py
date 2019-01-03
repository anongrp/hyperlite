""" Its all about processes and tasks  """

from enum import Enum
from threading import Thread

class ProcessType(Enum):
    Query = 1
    Writing = 2


class Process(Thread):
    def __init__(self):
        super().__init__(self)
        self.task_queue: list = []                 # List of Events

    def __exec(self, process_id: int):
        # Acquire Lock
        self.task_queue.remove(process_id)
        # Release Lock

    def run(self):
        for process_id in enumerate(self.task_queue):
            self.__exec(process_id)