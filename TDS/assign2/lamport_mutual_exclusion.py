import time
from heapq import heapify, heappush, heappop
import threading

nodelist = []
threads = []


def sleep_(t, func):
    time.sleep(t)
    func()


class node:
    def __init__(self, id, n, time_) -> None:
        self.id = id  # id of the node
        self.n = n  # total number of nodes in the system
        self.time = time_  # time of the node
        self.all = set()  # set of all nodes that have replied
        self.requests = []  # priority queue of requests
        heapify(self.requests)

    def broadcast(self, type):
        print(f"{self.id} : Broadcasting {type}  at time : {self.time}")
        for i in range(self.n):
            if i != self.id:
                nodelist[self.id].send(i, type)

    def enter(self):
        self.time += 1
        heappush(self.requests, (self.time, self.id))
        self.broadcast("request")

    def send(self, ind, type):
        nodelist[ind].receive((self.time, self.id, type))

    def check(self):
        if (
            len(self.all) == self.n - 1
            and len(self.requests) > 0
            and self.requests[0][1] == self.id
        ):
            print(f"{self.id} : Entering critical section  : {*self.requests,}")
            print(f"{self.id} : Exiting critical section")
            self.broadcast("release")

    def receive(self, data):
        print(f"{self.id} : receives a msg of {data[2].upper()} from {data[1]} at time : {data[0]}")

        if data[2] == "request":
            heappush(self.requests, (data[0], data[1]))

            def func():
                nodelist[self.id].send(data[1], "reply")

            threads.append(threading.Thread(target=sleep_, args=( 5, func,),))
            threads[-1].start()

        elif data[2] == "reply":
            self.all.add(data[1])
            self.check()

        elif data[2] == "release":
            t, id = heappop(self.requests)
            nodelist[id].all.clear()
            self.check()


num_process = int(input("Enter no of processes: "))

for i in range(num_process):
    nodelist.append(node(i, num_process, 0))

choice = "y"

while choice == "y":
    pid = int(input("Enter the node id which want to execute critical section: "))
    nodelist[pid].enter()
    choice = input("Does some other process want to execute cs? (y/n): ").lower()

for i in threads:
    i.join()
