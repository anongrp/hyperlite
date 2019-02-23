""" Event Loop The Heart Of HyperLite DB """
from queue import Queue
from .event import Event


class EventLoop:
    def __init__(self):
        # Used for RIDU operations
        self.query_processes = Queue()
        # Used for handle subscription for real time communication
        self.subscriptions = Queue()
        # Used for High Intense work Like: Saved to disk, defrag the database, database encryption
        self.system_process = Queue()

    def execute_sys_process(self):
        for i in range(0, self.system_process.qsize()):
            print("System Task Ack : " + str(self.system_process.get().exec()))

    def execute_query_process(self):
        for i in range(0, self.query_processes.qsize()):
            Event.emmit("on_task_complete", self.query_processes.get().exec())


class LoopRunner:
    def __init__(self):
        self.loop = EventLoop()
        self.isRunning: bool = self.shouldContinue()
        Event.on('loop-rerun', self.run)

    def run(self):
        while self.shouldContinue():
            self.isRunning = True
            self.loop.execute_query_process()
            self.loop.execute_sys_process()
        self.isRunning = False

    def shouldContinue(self) -> bool:
        return (self.loop.query_processes.qsize() != 0) or (self.loop.system_process.qsize() != 0) or (
                self.loop.subscriptions.qsize() != 0)
