"""
    Just for Testing purpose for now.

    After completion of Hyperlite server,
    It will contain the code which will interact with the driver.

"""

from hyperlite import event_loop, event
from hyperlite import process
from hyperlite import request_parser
from hyperlite import database
from hyperlite import collection

from server import Socket

if __name__ == "__main__":
    socker = Socket()
    loop_runner = event_loop.LoopRunner()
    loop_runner.run()

    db = database.Database('db-1')
    col = collection.Collection('col-1', db)
    data = request_parser.Parser.parse(data)
    process1 = process.Process(data)
    print(process1.exec())