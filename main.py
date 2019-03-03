"""
    Just for Testing purpose for now.
    After completion of Hyperlite server,
    It will contain the code which will interact with the driver.

"""

import os

import threading

from hyperlite import event_loop
from hyperlite.request_parser import Parser
from hyperlite.event import Event
from server import Socket
from hyperlite.collection import Collection, Collections
from hyperlite.process.process import renderProcess, renderRIDUProcess
from hyperlite import config

from storage_engine import initializer


def listenForConnection():
    Socket(config.DEFAULT.get('host'), config.DEFAULT.get('port')).listen()


def initMe():
    meta_col = None
    if os.path.exists(config.COLLECTION_PATH):
        meta_col = initializer.getCollection(config.COLLECTION_PATH)
        Collections.meta_collection = meta_col
    else:
        meta_col = Collection("hyperlite.col", "MetaData")
        Collections.meta_collection = meta_col



if __name__ == "__main__":
    initMe()
    # server_process = threading.Thread(target=listenForConnection)
    loop_runner = event_loop.LoopRunner()
    loop_runner.run()


    def manage_loop_status():
        if not loop_runner.isRunning:
            Event.emmit('loop-rerun')


    def onRequest(data):
        loop_runner.loop.query_processes.put(renderRIDUProcess(parsed_data=Parser.parse(data)))
        manage_loop_status()


    def onCollectionChange(collection: Collection):
        for proc in renderProcess(collection):
            loop_runner.loop.system_process.put(proc)
        manage_loop_status()


    Event.on('request', onRequest)
    Event.on('col-change', onCollectionChange)
    listenForConnection()
