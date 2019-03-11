import json
import socket

from hyperlite.event import Event
from hyperlite.logger import Log

TAG = "HDCP_Server"


class Socket(socket.socket):
    def __init__(self, host, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.clients = []
        Log.d(TAG, f"Server is Ready")

    def listen(self, **kwargs):
        super().bind((self.host, self.port))
        Log.i(TAG, f"Server is listening on port {self.port}")
        Event.on('on_task_complete', self.send_ack)
        while True:
            super().listen(1)
            client, addr = super().accept()
            Log.d(TAG, f"Client connected with {addr}")
            clientObj = {
                "client": client,
                "addr": addr
            }
            self.clients.append(clientObj)
            while True:
                try:
                    raw_query = str(client.recv(1024).decode("UTF-8"))
                    Log.d(TAG, f"Received data from client {addr}")
                    Log.d(TAG, f"Data -> {raw_query}")
                    if raw_query.lower() == 'exit':
                        client.close()
                        break
                    json_query = json.loads(raw_query)
                    json_query['addr'] = str(addr)
                    if json_query['type'] is not None and json_query['type'] == 'Request':
                        Event.emmit('request', json.dumps(json_query))
                        Log.d(TAG, f"Client is requesting for RIDU operation")
                    elif json_query['type'] is not None and json_query['type'] == 'Subscription':
                        Log.d(TAG, f"Client is requesting for subscription")
                        Event.emmit('req_sub', json.dumps(json_query))
                    elif json_query['type'] is not None and json_query['type'] == 'Pipeline':
                        Log.d(TAG, f"Client is requesting for Data Pipeline")
                        Event.emmit('req_pipe', json_query)
                    elif json_query['type'] is not None and json_query['type'] == 'Provider':
                        Log.d(TAG, f"Client is requesting for Provider Component")
                        Event.emmit('req_provider', json_query)

                    # code to communicate with hyperlite engine
                except ConnectionResetError as err:
                    Log.e(TAG, f"Connection Reset -> {err}")
                    client.close()
                    Log.d(TAG, f"{self.clients}")
                    self.clients.remove(clientObj)
                    Log.i(TAG, "Client removed from Clients list")
                    Log.d(TAG, f"Connected clients -> {self.clients if len(self.clients) != 0 else 'No Clients'}")
                    break
                except Exception as err:
                    Log.e(TAG, f"Connection broken -> {err}")
                    # errorSchema = """
                    # {
                    #     "type": "Error",
                    #     "message": "{}"
                    # }
                    # """.format(err)
                    # Log.d(TAG, errorSchema)
                    # client.send(errorSchema.encode('UTF-8'))
                    # client.close()
                    break

    def send_ack(self, ack):
        Log.d(TAG, f"Query Task ack -> {ack}")
        for client in self.clients:
            if str(client["addr"]) == ack["addr"]:
                Log.i(TAG, "Ack has send to client")
                client["client"].send(json.dumps(ack["Ack"]).encode("UTF-8"))
