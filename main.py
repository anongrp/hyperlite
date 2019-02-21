"""
    Just for Testing purpose for now.
    After completion of Hyperlite server,
    It will contain the code which will interact with the driver.

"""

from hyperlite import event_loop
from hyperlite import process
from hyperlite.request_parser import Parser
from hyperlite import config
from hyperlite.event import Event
from server import Socket
from hyperlite.collection import Collection
from hyperlite.process import write_process

if __name__ == "__main__":
    socket = Socket(config.DEFAULT.get('host'), config.DEFAULT.get('port'))
    loop_runner = event_loop.LoopRunner()
    loop_runner.run()


    def manage_loop_status():
        if not loop_runner.isRunning:
            Event.emmit('loop-rerun')

    def onRequest(data):
        loop_runner.loop.query_processes.append(process.Process(Parser.parse(data)))
        if not loop_runner.isRunning:
            Event.emmit('loop-rerun')

    def onCollectionChange(collection: Collection):
        loop_runner.loop.system_process.append(write_process.rendererProcess(collection))


    Event.on('request', onRequest)
    Event.on('col-change', onCollectionChange)

    socket.listen()

    # Code of releasing the F.A.L.T.U listeners
    Event.off('request')
    Event.off('col-change')

