from Crypto.PublicKey import RSA

def get_keys(RSA_modulus_length):
    key = RSA.generate(RSA_modulus_length)

    with open('RSA_modulus.txt','w') as f:
        f.write(str(key.n))
        f.close()