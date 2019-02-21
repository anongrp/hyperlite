""" Event Loop The Heart Of HyperLite DB """
from .event import Event


class EventLoop:
    def __init__(self):
        # Used for RIDU operations
        self.query_processes = []
        # Used for handle subscription for real time communication
        self.subscriptions = []
        # Used for High Intense work Like: Saved to disk, defrag the database, database encryption
        self.system_process = []

    def execute_sys_process(self):
        pass

    def execute_query_process(self):
        print(self.query_processes)
        for process in self.query_processes:
            print(process.exec())


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
        return (self.loop.query_processes.__len__() != 0) or (self.loop.system_process.__len__() != 0) or (
                    self.loop.subscriptions.__len__() != 0)
