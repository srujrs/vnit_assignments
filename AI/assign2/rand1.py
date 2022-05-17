import random

N = 50
edges = {}
adj = {}

perm = []

for i in range(1, 51):
    edges[i] = {}
    adj[i] = []
    
for i in range(50):
    x = random.randint(1, 50)
    while x in perm:
        x = random.randint(1, 50)
    perm.append(x)

for i in range(49):
    weight = random.randint(3, 15)
    edges[perm[i]][perm[i+1]] = weight
    edges[perm[i+1]][perm[i]] = weight

    print(perm[i], perm[i+1], weight)

weight = random.randint(3, 15)
edges[perm[0]][perm[49]] = weight
edges[perm[49]][perm[0]] = weight

print(perm[49], perm[0], weight)


for i in range(50):
    a = random.randint(1, 50)
    b = random.randint(1, 50)

    while b == a or b in edges[a]:
        b = random.randint(1, 50)

    weight = random.randint(20,50)

    edges[a][b] = weight
    edges[b][a] = weight
    print(a, b, weight)

for i in range(1, 51):
    for j in range(1, 51):
        if j in edges[i]:
            adj[i].append(edges[i][j])
        else:
            adj[i].append(0)

for i in adj:
    for j in adj[i]:
        print(j,end=',')
    print()


