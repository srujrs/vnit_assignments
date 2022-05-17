import threading
from time import sleep
import math
import sys  

class router:
    def __init__(self,name,TABLES,NETWORK):
        self.name = name
        self.dist_table = TABLES[name].copy()
        self.queue = {}

        self.adj_routers = []
        for i in NETWORK[name]:
            self.adj_routers.append(i)
            self.queue[i] = TABLES[i].copy()

# create distance table from the network graph stored in NETWORK
def getTable(name):
    table = {}

    global INFINITY
    global name_of_routers

    for i in name_of_routers:
        if i != name:
            # adding a list as [distance between those nodes, next hop to reach that node]
            if i in NETWORK[name]:
                table[i] = [NETWORK[name][i],i]
            else:
                table[i] = [INFINITY,'NAN']
            
    return table

# implementation of Bellman-Ford algorithm to calculate distance table and update them globally
def calculateDistances(name):
    global TABLES
    global UPDATED
    global ROUTERS_DICT

    # wait till adjacent routers send their updated distance TABLES
    while True:
        if len(ROUTERS_DICT[name].queue) == len(ROUTERS_DICT[name].adj_routers):
            break

    router_obj = ROUTERS_DICT[name]
    
    # check and update if there is a smaller cost path through a adjacent node
    for i in router_obj.dist_table:
        for j in router_obj.adj_routers:
            if j != i:
                cost = router_obj.dist_table[j][0] + router_obj.queue[j][i][0]
                if cost < router_obj.dist_table[i][0]:
                    router_obj.dist_table[i][0] = cost 
                    router_obj.dist_table[i][1] = router_obj.dist_table[j][1]
                    # add the edge details to the global updated dictionary
                    UPDATED[name].append(i)
    
    # update global dictionary
    TABLES[name] = router_obj.dist_table.copy()

    # add the updated table to adjacent router's queue
    for i in router_obj.adj_routers:
        ROUTERS_DICT[i].queue[name] = router_obj.dist_table.copy()

    # empty queue
    router_obj.queue = {}

    sleep(2)

# utility function to print the distance TABLES
def printTables():
    global TABLES
    for key in TABLES:
        print("--------------------------------------------")
        print("\tROUTER",key)
        print("--------------------------------------------")
        print("Node\tDistance\tNext Hop")
        print("--------------------------------------------")
        for i in TABLES[key]:
            print(i,"\t",end=" ")

            global INFINITY
            global UPDATED

            # if edge present in the global updated dictionary then put an astreix beside it
            if i in UPDATED[key]:
                if TABLES[key][i][0] != INFINITY:
                    print(TABLES[key][i][0],"*     \t",TABLES[key][i][1],"*")
                else:
                    print("INF*     \t",TABLES[key][i][1],"*")
                UPDATED[key].remove(i)
            else:
                if TABLES[key][i][0] != INFINITY:
                    print(TABLES[key][i][0],"      \t",TABLES[key][i][1])
                else:
                    print("INF      \t",TABLES[key][i][1])

# the global variables used 
INFINITY = math.inf
UPDATED = {}                    # holds data about recent updated connection distances
NETWORK = {}                    # holds data about the graph of network
TABLES = {}                     # holds the distance tables of all routers
ROUTERS_DICT = {}               # holds the router objects

file1 = open(sys.argv[1],'r')

num_of_routers = int(file1.readline())
name_of_routers = file1.readline().split()

for i in name_of_routers:
    NETWORK[i] = {}
    UPDATED[i] = []

string = file1.readline()
while string:
    temp = string.split()
    NETWORK[temp[0]][temp[1]] = int(temp[2])
    NETWORK[temp[1]][temp[0]] = int(temp[2])
    string = file1.readline()

file1.close()

# store distance tables
for i in name_of_routers:
    TABLES[i] = getTable(i)

# store router objects
for i in name_of_routers:
    ROUTERS_DICT[i] = router(i,TABLES,NETWORK)

print("\tITERATION ->",0)
printTables()

for _ in range(4):
    threads = []
    for i in name_of_routers:
        thread = threading.Thread(target=calculateDistances,args=(i))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("\n\n\tITERATION ->",_ + 1)
    printTables()
    