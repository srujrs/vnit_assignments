import socket    
import sys 
import random   


soc = socket.socket()        

port = int(sys.argv[1])               
 
soc.connect(('127.0.0.1', port))
print("Connected to server at", port)

soc.recv(1024).decode()

public_key = -1
with open('Alice_public_key.txt','r') as f:

    public_key = int(f.readline())
    print("\nAlice Public Key:\n", public_key)

    f.close()

n = -1
with open('RSA_modulus.txt','r') as f: 

    n = int(f.readline())
    print("\nRSA modulus:\n",n)

    f.close()

authorized = True

for round in range(3):

    print("\nROUND", round + 1, "\n")

    witness = int(soc.recv(8192).decode())
    print("\nWitness of Alice:\n", witness)

    challenge = random.randint(0, 1)

    soc.sendall(str(challenge).encode())
    print("\nChallenge given:\n", challenge)

    response = int(soc.recv(8192).decode())
    print("\nAlice's response:\n", response)

    if response == 0:
        authorized = False
        soc.sendall("NOT OK".encode())
    if ((response * response) - (witness * pow(public_key, challenge))) % n == 0:
        soc.sendall("OK".encode())
    else:
        authorized = False
        soc.sendall("NOT OK".encode())

if authorized:
    print("\nAlice is Verified successfully!\n")

soc.close()