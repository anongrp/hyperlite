""" Its all about processes and tasks  """

from threading import Thread


class Process(Thread):
    def __init__(self):
        super().__init__(self)
        self.task_queue: list = []                 # List of Events

    def __exec(self, event_id: int):
        event = self.task_queue[event_id]
        for task in event.events:
            event.emmit(task)
        self.task_queue.remove(event_id)

    def run(self):
        for event_id in enumerate(self.task_queue):
            self.__exec(event_id)
