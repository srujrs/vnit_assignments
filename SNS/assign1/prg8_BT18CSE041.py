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
        
def binary_extended_gcd(x, y):
    g = 1
    res = []

    while x % 2 == 0 and y % 2 ==0:
        x = x // 2
        y = y // 2
        g = 2*g

    u, v, A, B, C, D = x, y, 1, 0, 0, 1

    while True:
        while u % 2 == 0:
            u = u // 2

            if A % 2 == 0 and B % 2 == 0:
                A = A // 2
                B = B // 2
            else:
                A = (A + y) // 2
                B = (B - x) // 2
        
        while v % 2 == 0:
            v = v // 2

            if C % 2 == 0 and D % 2 == 0:
                C = C // 2
                D = D // 2
            else:
                C = (C + y) // 2
                D = (D - x) // 2
        
        if u >= v:
            u = u - v 
            A = A - C
            B = B - D 
        else:
            v = v - u 
            C = C - A 
            D = D - B 
        
        if u == 0:
            a = C 
            b = D 
            
            res = [g*v, a, b]

            break 

    return res 

def multiplicative_inverse(a, m):
    res = binary_extended_gcd(a, m)

    if res[0] > 1:
        return -1
    else:
        return res[1]

def garner_algo_CRT(t, M, v):
    C = [1] * t 

    for i in range(1, t):
        for j in range(i):
            u = multiplicative_inverse(M[j], M[i])
            C[i] = (u*C[i]) % M[i]

    u = v[0]
    x = u

    for i in range(1, t):
        u = ((v[i] - x)*C[i]) % M[i]
        temp_m_product = 1
        for i in range(i):
            temp_m_product *= m[i]
        x = x + u * temp_m_product
        # print(i,u,x)

    # print(C)

    return x 

input_abm = [int(x) for x in sys.argv[1:]]

a = [0] * input_abm[0]
b = [0] * input_abm[0]
m = [0] * input_abm[0]

alphaBAR_beta = [0] * input_abm[0]
myu = [0] * input_abm[0]

found = True

for i in range(input_abm[0]):
    a[i] = input_abm[3*i + 1]
    b[i] = input_abm[3*i + 2]
    m[i] = input_abm[3*i + 3]

for x in range(input_abm[0] - 1):
    for y in range(x + 1, input_abm[0]):
        if gcd(m[y], m[x]) != 1:
            found = False
            break

if found:
    for i in range(input_abm[0]):
        g = gcd(a[i], m[i])

        if b[i] % g == 0:
            alpha = a[i] // g 
            beta = b[i] // g
            myu[i] = m[i] // g 

            alphaBAR_beta[i] = beta * multiplicative_inverse(alpha, myu[i])
            while alphaBAR_beta[i] < 0:
                alphaBAR_beta[i] += myu[i]

        else:
            found = False
            break

if found:
    print("Y",garner_algo_CRT(input_abm[0], myu, alphaBAR_beta), end="")
else:
    print("N", end="")

