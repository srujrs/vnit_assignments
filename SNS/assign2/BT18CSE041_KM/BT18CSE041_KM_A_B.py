import socket
import random

import BT18CSE041_KM_A_Kg as Kg
import BT18CSE041_KM_A_En as En 
import BT18CSE041_KM_A_De as De


def start_socket(host, port):
    bob_soc = socket.socket()
    bob_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    bob_soc.bind((host, port)) 
    print ("Socket started at port: %s" %(port))

    return bob_soc


host = '127.0.0.1'
port = 12347
kdc_port = 12345

bob_soc = start_socket(host, port)

print("\nBob setting up symmetric key with KDC.......\n")
bob_soc.connect(('127.0.0.1', kdc_port))  
Kg.generate_key("KBT")
bob_soc.sendall("KBT".encode())
bob_soc.close()

bob_soc = start_socket(host, port)

bob_soc.listen()            

print("\nReceiving shared key from Alice in KBT encryption.........\n")
alice, alice_addr = bob_soc.accept()
cipher_txt = alice.recv(5120).decode()

data = (De.DES_CBC_decrypt(cipher_txt, "KBT").decode()).split("b/b")

shared_key_file = data[0]
alice_port = data[1]

print("\nSending Nonce B to Alice with shared key encryption.........\n")
nonce_B = random.randint(1, 1000)
alice.send(En.DES_CBC_encrypt(str(nonce_B), shared_key_file).encode())

print("\nReceiving Alice's response encrypted with shared key..........\n")
response = int(alice.recv(1024).decode())

if response == nonce_B - 1:
    print("\nNonce B verified!\n")

alice.send("ACK".encode())

print("\nReceiving mssg from Alice...........\n")

cipher_txt = alice.recv(1024).decode()
print("\nCipher txt:\n", cipher_txt)

mssg = De.DES_CBC_decrypt(cipher_txt, shared_key_file).decode()
print("\nPlain txt:\n", mssg)


bob_soc.close()