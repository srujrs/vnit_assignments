from collections import defaultdict, deque


class Graph:
    def __init__(self, n):
        self.graph = defaultdict(lambda: [])
        self.vertices = n
        self.edges = 0
        self.toposorted = []
        self.vertix = set()

    def addEdge(self, a, b):  # tested
        self.vertix.add(a)
        self.vertix.add(b)
        self.graph[a].append(b)
        self.edges += 1

    def topologicalSort(self):  # tested
        in_degree = defaultdict(lambda: 0)
        for i in self.graph:
            for j in self.graph[i]:
                in_degree[j] += 1
        queue = deque()
        for i in self.vertix:
            if in_degree[i] == 0:
                queue.append(i)
        cnt = 0
        while queue:
            u = queue.popleft()
            self.toposorted.append(u)
            for i in self.graph[u]:
                in_degree[i] -= 1
                if in_degree[i] == 0:
                    queue.append(i)
            cnt += 1
        if cnt != self.vertices:
            return False
        else:
            return True


def print_clocks(clocks):
    for name, i in clocks:
        print(f"{name}: ", end="")
        print(*i, sep=" ---------------- ")
        print()


num_process = int(input("Enter the number of processes: "))

total_events = 0
clocks = []
g = Graph(num_process)

for i in range(num_process):
    proc_num = "p" + str(i+1)
    print("For process", proc_num, end=', ')

    events_num = int(input("Enter the number of events: "))
    
    for j in range(1, events_num):
        g.addEdge((i + 1, j), (i + 1, j + 1))

    clocks.append((proc_num, [x for x in range(1, events_num + 1)]))
    total_events += events_num

events = defaultdict(lambda: [])
num_mssgs = int(input("Enter the number of messages: "))

for _ in range(num_mssgs):
    pid, eid = map(int, input("Enter the process id and event id for the sender : ").split())
    pid2, eid2 = map(int, input("Enter the process id and event id for the receiver : ").split())

    g.addEdge((pid, eid), (pid2, eid2))
    events[(pid, eid)] = (pid2, eid2)

g.topologicalSort()

for pid, eid in g.toposorted:
    if (pid, eid) in events:
        pid2, eid2 = events[(pid, eid)]
        if clocks[pid - 1][1][eid - 1] >= clocks[pid2 - 1][1][eid2 - 1]:
            extra = clocks[pid - 1][1][eid - 1] - clocks[pid2 - 1][1][eid2 - 1] + 1
            for i in range(eid2 - 1, len(clocks[pid2 - 1][1])):
                clocks[pid2 - 1][1][i] += extra

print_clocks(clocks)
