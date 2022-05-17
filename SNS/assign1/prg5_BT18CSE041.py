import sys
from math import sqrt

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

a, x, n = map(int, sys.argv[1:])

is_n_prime = True
for i in range(2, int(sqrt(n)) + 1):
    if n % i == 0:
        is_n_prime = False
        break 

if is_n_prime:
    # print("Trying to reduce power by Euler's Fermat's theorem generalization!")

    new_reduced_power = x % phi_n

    # print("\t{}^{} mod {} reduced to {}^{} mod {} as {}^{} mod {} is 1 by theorem".format(a, x, n, a, new_reduced_power, n, a, x // phi_n, n))
    # print("Now we use Repeated square-and-multiply algorithm for exponentiation in Z to solve the simple mod!")

    print(square_n_multiply_algo(a, new_reduced_power, n),end="")

else:
    # print("No application of Euler's Fermat's theorem generalization possible directly but cab used in reducing computations!")
    res = 1
    new_reduced_power = x

    while True:
        if n > x:
            break
        else:
            res = res * square_n_multiply_algo(a, new_reduced_power % (n-1),n)
            new_reduced_power = int(new_reduced_power / (n-1))
            a = square_n_multiply_algo(a, (n-1), n)

    print(res*square_n_multiply_algo(a, new_reduced_power, n),end="")
