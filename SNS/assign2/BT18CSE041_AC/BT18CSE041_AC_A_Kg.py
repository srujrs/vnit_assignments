from Crypto.PublicKey import RSA

def get_keys(RSA_modulus_length):
    key = RSA.generate(RSA_modulus_length)

    RSA_modulus = key.n
    RSA_public_key = key.e
    RSA_private_key = key.d

    return [RSA_modulus, RSA_public_key, RSA_private_key]

# def gcd(a, b):
#     if a >= b:
#         while b != 0:
#             r = a % b
#             a = b 
#             b = r 
#         return a 
    
#     else:
#         return gcd(b, a)

# def get_key():
#     p = 897401
#     q = 36137

#     n = p*q

#     e = 2
#     phi = (p-1)*(q-1)
#     while e < phi:
#         if gcd(e, phi) == 1:
#             break
#         else:
#             e += 1

#     k = 2
#     d = (1 + (k*phi)) // e

#     print(n,d,e)

#     RSA_modulus = n
#     RSA_public_key = e
#     RSA_private_key = d
