import sys

def gcd(a, b):
    if a >= b:
        while b != 0:
            r = a % b
            a = b 
            b = r 
        return a 
    
    else:
        return gcd(b, a)

a, m = map(int, sys.argv[1:])

res = 1

if gcd(a, m) == 1:
    prod = 1

    for i in range(1, m):
        prod = ((a % m) * prod) % m
        if prod == 1:
            res = i
            break

else:
    res = -1

print(res, end="")