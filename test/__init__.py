import time
import queue
if __name__ == "__main__":
    print("\t\t\t ### HyperLite DB ### \n\n\n")

    processes = queue.Queue()
    for i in range(0, 10):
        processes.put(time.time())
    print("Queue size : " + str(processes.qsize()))
    for i in range(0, processes.qsize()):
        print(processes.get())
    print("Queue size : " + str(processes.qsize()))
