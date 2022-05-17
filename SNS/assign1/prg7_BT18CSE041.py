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

def extended_gcd_util(a, b):
    gcd_and_coeff = [0, 0, 0]

    if b == 0:
        # d←a, x←1, y←0, and return(d,x,y)
        gcd_and_coeff[0] = a
        gcd_and_coeff[1] = 1
        gcd_and_coeff[2] = 0
    else:
        # x2←1, x1←0, y2←0, y1←1
        x2, x1, y2, y1 = 1, 0, 0, 1

        while b > 0:
            # q←[a/b], r←a − qb, x←x2 − qx1, y←y2 − qy1
            q = a//b
            r, gcd_and_coeff[1], gcd_and_coeff[2] = a - q*b, x2 - q*x1, y2 - q*y1

            # a←b, b←r, x2←x1, x1←x, y2←y1, and y1←y
            a, b, x2, x1, y2, y1 = b, r, x1, gcd_and_coeff[1], y1, gcd_and_coeff[2] 
        
        # d←a, x←x2, y←y2, and return(d,x,y)
        gcd_and_coeff[0], gcd_and_coeff[1], gcd_and_coeff[2] = a, x2, y2 

    return gcd_and_coeff

def extended_gcd(a, b):
    if a >= 0 and b >= 0: 
        return extended_gcd_util(a, b)
        
def multiplicative_inverse(a, m):
    res = extended_gcd(a, m)

    if res[0] > 1:
        return -1
    else:
        return res[1]


a, b, m = map(int, sys.argv[1:])

g = gcd(a, m)

if b % g == 0:
    alpha = a // g 
    beta = b // g
    myu = m // g 

    print("Y", g, end=" ")

    a_of_AP = beta * multiplicative_inverse(alpha, myu)
    while a_of_AP < 0:
        a_of_AP += (((-a_of_AP) // myu) + 1) * myu

    for k in range(g - 1):
        print(a_of_AP + k*myu, end=" ")
    
    print(a_of_AP + (g - 1)*myu, end="")

else:
    print("N", end="")