import random

N = 50

edges = {}
adj = {}

for i in range(1, N+1):
    edges[i] = {}
    adj[i] = []

for i in range(1,N):
    for j in range(i+1, N + 1):
        weight = random.randint(20,50)
        edges[i][j] = weight
        edges[j][i] = weight
        print(i, j, weight)

for i in range(1, N+1):
    for j in range(1, N+1):
        if j in edges[i]:
            adj[i].append(edges[i][j])
        else:
            adj[i].append(0)

for i in adj:
    for j in adj[i]:
        print(j,end=',')
    print()
