import json
import socket

from hyperlite.event import Event


class Socket(socket.socket):
    def __init__(self, host, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.clients = []

    def listen(self, **kwargs):
        super().bind((self.host, self.port))
        print("Server is listening on port {}".format(self.port))
        while True:
            super().listen(1)
            client, addr = super().accept()
            self.clients.append({
                "client": client,
                "addr": addr
            })
            while True:
                raw_query = client.recv(1024).decode("UTF-8")
                if raw_query.lower() == 'exit':
                    client.close()
                    break
                json_query = json.load(raw_query)
                if json_query.type is not None and json_query.type.lower() == 'Request':
                    Event.emmit('request', json_query)
                # code to communicate with hyperlite engine

    def on_request(self, callback):
        Event.on("request", callback)
