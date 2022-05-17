import sys

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

a, m = map(int, sys.argv[1:])
res = extended_gcd(a, m)

if res[0] > 1:
    print("N", end="")
else:
    while res[1] < 0:
        res[1] += (((-res[1]) // m) + 1) * m
    print("Y", res[1], end="")
   