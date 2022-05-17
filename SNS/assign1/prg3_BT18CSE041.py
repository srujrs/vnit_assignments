import sys 
from math import sqrt

num = int(sys.argv[1])

ans = []

is_num_prime = True
for i in range(2, int(sqrt(num)) + 1):
    if num % i == 0:
        is_num_prime = False
        break

if is_num_prime:
    print(num)

else:
    for i in range(2, num//2 + 1):
        if i > num:
            break
        else:
            is_i_prime = True
            for j in range(2, int(sqrt(i)) + 1):
                if i % j == 0:
                    is_i_prime = False
                    break
            if is_i_prime:
                while num % i == 0:
                    ans.append(i)
                    num = num/i 

size = len(ans)
for i in range(size - 1):
    print(ans[i], end=" ")
print(ans[size - 1],end="")