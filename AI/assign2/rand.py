import random

N = 5
edges = {}
adj = {}

perm = []

for i in range(1, N + 1):
    edges[i] = {}
    adj[i] = []

for i in range((N*(N-1))//2):
    a = random.randint(1, N)
    b = random.randint(1, N)

    while b == a or b in edges[a]:
        b = random.randint(1, N)

    weight = random.randint(20,50)

    edges[a][b] = weight
    edges[b][a] = weight
    print(a, b, weight)

# for i in range(1, 51):
#     for j in range(1, 51):
#         if j in edges[i]:
#             adj[i].append(edges[i][j])
#         else:
#             adj[i].append(0)

# for i in adj:
#     for j in adj[i]:
#         print(j,end=',')
#     print()


