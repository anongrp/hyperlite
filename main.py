"""
    Just for Testing purpose for now.
    After completion of Hyperlite server,
    It will contain the code which will interact with the driver.

"""

import os

from multiprocessing import Process, Manager

from hyperlite import event_loop
from hyperlite import process
from hyperlite.request_parser import Parser
from hyperlite.event import Event
from server import Socket
from hyperlite.collection import Collection, Collections
from hyperlite.process import process
from hyperlite import config

from storage_engine import initializer


def listenForConnection():
    Socket(config.DEFAULT.get('host'), config.DEFAULT.get('port')).listen()


def initMe():
    if os.path.exists(config.COLLECTION_PATH):
        col = initializer.getCollection(config.COLLECTION_PATH)
        Collections.meta_collection = col
    else:
        Collections.meta_collection = Collection("hyperlite.col", "MetaData")


if __name__ == "__main__":
    initMe()
    server_process = Process(target=listenForConnection)
    loop_runner = event_loop.LoopRunner()
    loop_runner.run()


    def manage_loop_status():
        if not loop_runner.isRunning:
            Event.emmit('loop-rerun')


    def onRequest(data):
        loop_runner.loop.query_processes.append(process.Process(Parser.parse(data)))
        manage_loop_status()


    def onCollectionChange(collection: Collection):
        for proc in process.renderProcess(collection):
            loop_runner.loop.system_process.append(proc)
        manage_loop_status()


    server_process.start()
    Event.on('request', onRequest)
    Event.on('col-change', onCollectionChange)
    server_process.join()
    print("software is free")
