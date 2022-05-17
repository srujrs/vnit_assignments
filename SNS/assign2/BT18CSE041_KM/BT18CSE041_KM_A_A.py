import socket
import random

import BT18CSE041_KM_A_Kg as Kg
import BT18CSE041_KM_A_En as En 
import BT18CSE041_KM_A_De as De


def start_socket(host, port):
    alice_soc = socket.socket()
    alice_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    alice_soc.bind((host, port)) 
    print ("Socket started at port: %s" %(port))

    return alice_soc


host = '127.0.0.1'
port = 12346
kdc_port = 12345
bob_port = 12347

alice_soc = start_socket(host, port)

print("\nAlice setting up symmetric key with KDC.....\n")
alice_soc.connect(('127.0.0.1', kdc_port))  
Kg.generate_key("KAT")
alice_soc.sendall("KAT".encode())

print("\nSending A port, B port and Nonce A num to KDC.....\n")
alice_soc.sendall(str(port).encode())  
alice_soc.recv(3).decode()
alice_soc.sendall(str(bob_port).encode())
alice_soc.recv(3).decode()
nonce_A = random.randint(1, 1000)
alice_soc.sendall(str(nonce_A).encode())

print("Receiving KDC's response having shared key.....\n")
cipher_txt = alice_soc.recv(8192).decode()
data = (De.DES_CBC_decrypt(cipher_txt, "KAT").decode()).split("b/b")

if nonce_A == data[0]:
    print("\nNonce A verified!\n")

shared_key_file = data[2]
encrypted_mssg_to_bob = data[3]

alice_soc.close()

print("\nSending shared key to Bob encrypted with KBT given by KDC.....\n")
alice_soc = start_socket(host, port)

alice_soc.connect(('127.0.0.1', bob_port))
alice_soc.sendall(encrypted_mssg_to_bob.encode())

print("\nReceiving Nonce B from Bob encrypted with shared key.....\n")
cipher_txt = alice_soc.recv(1024)
nonce_B = int(De.DES_CBC_decrypt(cipher_txt, shared_key_file))

print("\Sending Nonce B - 1 to Bob with shared key encryption.....\n")
alice_soc.sendall(str(nonce_B - 1).encode())

alice_soc.recv(3).decode()

print("\nSending mssg to Bob.....\n")
mssg = "Hello there Bob!"
print("\nPlain txt:\n", mssg)

cipher_txt = En.DES_CBC_encrypt(mssg, shared_key_file)
print("\nCipher txt:\n", cipher_txt)

alice_soc.sendall(cipher_txt.encode())


alice_soc.close()