import socket

import BT18CSE041_KM_A_Kg as Kg
import BT18CSE041_KM_A_En as En

kdc_soc = socket.socket()
kdc_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '127.0.0.1'
port = 12345
alice_port = 0
bob_port = 0

kdc_soc.bind((host, port)) 
print ("KDC started at port: %s" %(port))

kdc_soc.listen()       

print("\nBob setting up symmetric key with KDC..........\n")
bob, bob_addr = kdc_soc.accept()
bob_key_file = bob.recv(1024).decode()
bob.close()
 
print("\nAlice setting up symmetric key with KDC........\n")
alice, alice_addr = kdc_soc.accept()
alice_key_file = alice.recv(1024).decode()

print("\nReceiving Nonce A and Bob's port from Alice........\n")
alice_port = int(alice.recv(1024).decode())
alice.send("ACK".encode())
bob_port = int(alice.recv(1024).decode())
alice.send("ACK".encode())
nonce_A = int(alice.recv(1024).decode())

print("\nGenerating shared key.........\n")
shared_key_file = "shared_key"
Kg.generate_key(shared_key_file)

alice.send(
    En.DES_CBC_encrypt(
        str(nonce_A) + "b/b" +
        str(bob_port) + "b/b" +
        shared_key_file + "b/b" +
        str(En.DES_CBC_encrypt(
            shared_key_file + "b/b" +
            str(alice_port), bob_key_file))
        , alice_key_file).encode()
)
alice.close()


kdc_soc.close()