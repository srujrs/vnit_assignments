import socket 
import sys    
import random

import BT18CSE041_EA_A_Kdc as Kdc


def gcd(a, b):
    if a >= b:
        while b != 0:
            r = a % b
            a = b 
            b = r 
        return a 
    
    else:
        return gcd(b, a)


soc = socket.socket()        
 
port = int(sys.argv[1])            
 
soc.bind(('', port))        
print ("Socket started at port: %s" %(port))
 
soc.listen()            
 
client, addr = soc.accept()    
print ('Got connection from', addr)

Kdc.get_keys(1024)

n = -1
with open('RSA_modulus.txt','r') as f:

    n = int(f.readline())
    print("\nRSA modulus:\n",n)

    f.close()

secret = random.randint(1, n - 1)
while gcd(n,secret) != 1:
    secret = random.randint(1, n - 1)

public_key = pow(secret, 2, n)

with open('Alice_public_key.txt','w') as f:

    f.write(str(public_key))
    print("\nPublic key of Alice:\n", public_key)
    f.close()

client.send("Setup done".encode())

for round in range(3):
    print("\nROUND", round + 1, "\n")

    r = random.randint(1, n - 1)
    
    x = pow(r, 2, n)
    print("\nWitness of Alice:\n", x)

    client.send(str(x).encode())
    
    challenge = int(client.recv(3).decode())
    print("\nChallenge to Alice:\n", challenge)

    y = r
    if challenge == 1:
        y = (r*secret) % n

    client.send(str(y).encode())

    print("\nResponse of Alice:\n", y)

    reply = client.recv(6).decode()

    print("\nBob's reply:\n", reply)

soc.close()