"""
    Just for Testing purpose for now.

    After completion of Hyperlite server,
    It will contain the code which will interact with the driver.

"""

from hyperlite import event_loop
from hyperlite import process
from hyperlite.request_parser import Parser
from hyperlite import database
from hyperlite import collection
from hyperlite import config
from hyperlite.event import Event
from server import Socket

if __name__ == "__main__":
    socket = Socket(config.DEFAULT.host, config.DEFAULT.port)
    socket.listen()
    loop_runner = event_loop.LoopRunner()
    loop_runner.run()

    db = database.Database('db-1')
    col = collection.Collection('col-1', db)

    Event.on('request', lambda data: process.Process(Parser.parse(data)))
