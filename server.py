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
        Event.on('on_task_complete', self.send_ack)
        while True:
            super().listen(1)
            client, addr = super().accept()
            self.clients.append({
                "client": client,
                "addr": addr
            })
            while True:
                try:
                    raw_query = str(client.recv(1024).decode("UTF-8"))
                    if raw_query.lower() == 'exit':
                        client.close()
                        break
                    json_query = json.loads(raw_query)
                    json_query['addr'] = str(addr)
                    if json_query['type'] is not None and json_query['type'] == 'Request':
                        Event.emmit('request', json.dumps(json_query))
                        # if self.onRequestCallback is not None:
                        #     self.onRequestCallback(json_query)
                    # code to communicate with hyperlite engine
                except Exception as err:
                    client.close()
                    break

    def send_ack(self, ack):
        print("Query Task ack: ", ack)
        for client in self.clients:
            if str(client["addr"]) == ack["addr"]:
                print("Ack has send to client")
                client["client"].send(json.dumps(ack["Ack"]).encode("UTF-8"))
