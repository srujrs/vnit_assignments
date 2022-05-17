import sys
from math import sqrt 

def gcd(a, b):
    if a >= b:
        while b != 0:
            r = a % b
            a = b 
            b = r 
        return a 
    
    else:
        return gcd(b, a)

num = int(sys.argv[1])

RRSM_m = []

is_num_prime = True
for i in range(2, int(sqrt(num)) + 1):
    if num % i == 0:
        is_num_prime = False
        break 

if is_num_prime:
    for i in range(1, num):
        RRSM_m.append(i)
    
    for i in RRSM_m:
        print(i % num, end=" ")

    print(num - 1,end="")

else:
    if num % 2 == 0:
        phi_num = 0
        for i in range(num + 1, 2*num, 2):
            if gcd(i, num) == 1:
                RRSM_m.append(i)
                phi_num += 1
        
        for i in RRSM_m:
            print(i % num, end=" ")

        print(phi_num,end="")
        
    else:
        phi_num = 0
        for i in range(num + 1, 2*num):
            if gcd(i, num) == 1:
                RRSM_m.append(i)
                phi_num += 1

        for i in RRSM_m:
            print(i % num, end=" ")

        print(phi_num,end="")