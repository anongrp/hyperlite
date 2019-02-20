""" Event Loop The Heart Of HyperLite DB """

from .process import Process

class EventLoop:
    def __init__(self):
        self.user_process: Process = []
        self.system_process: Process = []

    def execute_sys_process(self):
        self.events.clear()
        pass

    def execute_usr_process(self):
        self.callbacks.clear()
        pass


class LoopRunner:
    def __init__(self):
        self.loop = EventLoop()

    def run(self):
        while(self.shouldContinue()):
            self.loop.execute_usr_process()
            self.loop.execute_sys_process()

    def shouldContinue(self) -> bool:
        return (self.loop.user_process.__len__() != 0) or (self.loop.system_process.__len__() != 0)
