import sys
sys.path.append('..')
from hyperlite.process import Process
from hyperlite.request_parser import Parser
from hyperlite.collection import Collection
from hyperlite.database import Database
import socket


# def goto(linenum):  #a simple implementation of goto statement for easily writing code
#     global line
#     line = linenum


def Main():
    global line
    line = 1

    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host, port))

    with open('test2.json', 'r') as f1:  # taking the user's data file to store
        data = f1.read()

    while True:
        print("Server listening!!!!")

        # listening to 1 client at a time
        s.listen(1)
        # accepting a clients request when he run connect() function
        c, addr = s.accept()

        print(type(addr))
        print("Connection from: " + str(addr))

        # queries = []
        # for testing, populating the queries list
        queries = [
            # "db= Database('db-1')",  
            # "col = Collection('col-1', db)",
            # 'data = Parser.parse(data)',
            # 'process1= Process(data)',
            # 'process1.exec()',
        ]

        # start an indefinite connection, (till explicitly terminated)
        while True:
            client_command = c.recv(1024).decode('utf-8')

            if not data or 'end connection' in client_command:
                break

            if 'execute' in client_command:
                for code in queries:
                    print(code)
                    exec(code)  # this will execute the client commands
                    # empty the list after executing the code
                queries = []
            else:
                queries.append(client_command)

            for lines in queries:
                print("----> " + str(lines))

            print("From connected user: " + client_command)
                # c.send(data.encode('utf-8'))
            

    c.close()

if __name__ == '__main__':
    Main()



