# from hyperlite import event_loop, event
from hyperlite import process
from hyperlite import request_parser
from hyperlite import database
from hyperlite import collection

if __name__ == "__main__":
    # loop_runner = event_loop.LoopRunner()
    # loop_runner.run()

    with open('test/test2.json', 'r') as f1:
        data = f1.read()

    db = database.Database('db-1')
    col = collection.Collection('col-1', db)
    data = request_parser.Parser.parse(data)
    process1 = process.Process(data)
    process1.exec()

    with open('test/test.json', 'r') as f:
        data = f.read()
    data = request_parser.Parser.parse(data)
    process2 = process.Process(data)
    output_data = process2.exec()
    for data in output_data:
        print(data)
