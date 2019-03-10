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
from hyperlite.logger import Log
from storage_engine import initializer

TAG = "Main_Process"  # Constant used just for logging


def listenForConnection():
    Socket(config.DEFAULT.get('host'), config.DEFAULT.get('port')).listen()


def initMe():
    Log.c(TAG, "Starting Hyperlite Database")
    Log.w(TAG, f"We are running on {config.PLATFORM} Operating System")
    Log.i(TAG, f"Database files can be found on {config.DATABASE_PATH} ")
    if os.path.exists(config.COLLECTION_PATH):
        meta_col = initializer.getCollection(config.COLLECTION_PATH)
        Collections.meta_collection = meta_col
        Log.i(TAG, "Meta collection found on disk")
    else:
        meta_col = Collection("hyperlite.col", "MetaData")
        Collections.meta_collection = meta_col
        Log.w(TAG, "Meta collection file not found so creating new meta collection")


if __name__ == "__main__":
    initMe()
    # server_process = threading.Thread(target=listenForConnection)
    loop_runner = event_loop.LoopRunner()
    loop_runner.run()

    def manage_loop_status():
        if not loop_runner.isRunning:
            Log.i(TAG, "EventLoop is stopped, Rerunning EventLoop...")
            Event.emmit('loop-rerun')


    def onRequest(data):
        Log.d(TAG, f"New request - {data}")
        loop_runner.loop.query_processes.put(renderRIDUProcess(parsed_data=Parser.parse(data)))
        manage_loop_status()


    def onSubscription(data):
        Log.d(TAG, f"New subscription request - {data}")
        # TODO: Adding subscription plan
        loop_runner.loop.subscriptions.put()


    def onCollectionChange(collection: Collection):
        Log.i(TAG, "Event -> Collection Changed")
        for proc in renderProcess(collection):
            loop_runner.loop.system_process.put(proc)
        for proc in renderProcess(Collections.meta_collection):
            loop_runner.loop.system_process.put(proc)
        manage_loop_status()


    Event.on('request', onRequest)
    Event.on('col-change', onCollectionChange)
    Event.on('req_sub', onSubscription)
    listenForConnection()
