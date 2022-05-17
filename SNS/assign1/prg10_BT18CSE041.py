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

def get_prime_factors(num):
    prime_factors = []

    is_num_prime = True
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            is_num_prime = False
            break

    if is_num_prime:
        prime_factors.append(num)

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
                    prime_factors.append(i)
                    while num % i == 0:
                        num = num/i 

    return prime_factors

def get_phi_m(num):
    res = 0

    is_num_prime = True
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            is_num_prime = False
            break 

    if is_num_prime:
        res = num - 1

    else:
        if num % 2 == 0:
            phi_num = 0
            for i in range(num + 1, 2*num, 2):
                if gcd(i, num) == 1:
                    phi_num += 1
            
            res = phi_num
            
        else:
            phi_num = 0
            for i in range(num + 1, 2*num):
                if gcd(i, num) == 1:
                    phi_num += 1
            res = phi_num

    return res

def get_primitive_roots(num):
    prim_roots = []

    phi_m = get_phi_m(num)
    prime_factors = get_prime_factors(phi_m)

    for a in range(2, phi_m + 1):
        found = False

        for i in prime_factors:
            base = a 
            exponent = phi_m // i
            mod_num = num

            pow = 1 
            base = base % mod_num 

            while exponent > 0:
                if exponent % 2 == 1:
                    pow = (pow * base) % mod_num

                exponent = exponent // 2
                base = (base * base) % mod_num

            if pow == 1:
                found = True
                break
             
        if not found:
            prim_roots.append(a)

    return prim_roots

def square_n_multiply_algo(a, x, n):
    b = 1
    temp_new_x = x
    new_x_binary = ''
    while temp_new_x > 0:
        new_x_binary += str(temp_new_x % 2)
        temp_new_x = temp_new_x // 2

    A = a 
    if new_x_binary[0] == '1':
        b = a 
    
    for i in range(1, len(new_x_binary)):
        A = (A*A) % n 
        if new_x_binary[i] == '1':
            b = (A*b) % n

    return b

def order_modulo_m(a, m):
    res = -1

    for i in range(1, m):
        if square_n_multiply_algo(a, i, m) == 1:
            res = i
            break

    return res 

num = int(sys.argv[1])

is_num_prime = True
for i in range(2, int(sqrt(num)) + 1):
    if num % i == 0:
        is_num_prime = False
        break

res = []

if is_num_prime and num > 2:
    res = get_primitive_roots(num)

else:
    phi_num = get_phi_m(num)

    for i in range(num):
        if order_modulo_m(i, num) == phi_num:
            res.append(i)

size = len(res)

if size != 0:
    print(size, end=" ")

    for i in range(size - 1):
        print(res[i], end=" ")
    print(res[size - 1], end="")

else:
    print(0, end="")


        