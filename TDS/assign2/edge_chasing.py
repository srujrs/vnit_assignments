from collections import deque


class Process:
    def __init__(self, id) -> None:
        self.id = id
        self.dependencies = []
        self.probe = None
        

num_process = int(input("Enter the number of total Processes: "))
processes = [Process(i+1) for i in range(num_process)]
num_edges = int(input("Enter the number of total Edges in dependency graph: "))

for _ in range(num_edges):
    u, v = map(int, input("Enter the edge i->j if i depends on j: ").split())
    processes[u].dependencies.append(v)

ini = int(input("Enter the Initiator Process:"))

q = deque()
for i in processes[ini].dependencies:
    q.append(i)
    processes[i].probe = (ini, ini, i)

deadlock = -1
while(len(q) > 0 and deadlock < 0):
    temp = q.popleft()
    initiator, sender, receiver = processes[temp].probe
    for i in processes[temp].dependencies:
        processes[i].probe = (initiator, temp, i)
        if(initiator == i):
            deadlock = i
            break
        q.append(i)

if(deadlock < 0):
    print("No Deadlock!")
else:
    print("Deadlock exists!")

    probe = processes[deadlock].probe
    lock = deque([deadlock])
    while(probe[0] != probe[1]):
        sender = probe[1]
        lock.appendleft(sender)
        probe = processes[sender].probe

    lock.appendleft(probe[0])
    lock = list(lock)
    print(*lock, sep=" -> ")
