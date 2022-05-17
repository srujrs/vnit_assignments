import socket    
import sys    

import BT18CSE041_AC_A_En as En
import BT18CSE041_AC_A_De as De


soc = socket.socket()        

port = int(sys.argv[1])               
 
soc.connect(('127.0.0.1', port))
print("Connected to server at", port)
 
cipher_txt = soc.recv(1024).decode()
cipher_txt = int(cipher_txt, 16)

print("\nCipher text:")
print(cipher_txt)

soc.sendall("ACK".encode())

k0 = soc.recv(1024).decode()
k0 = int(k0, 16)

soc.sendall("ACK".encode())

k1 = soc.recv(1024).decode()
k1 = int(k1, 16)

soc.sendall("ACK".encode())

RSA_modulus = soc.recv(1024).decode()
RSA_modulus = int(RSA_modulus, 16)

soc.sendall("ACK".encode())

RSA_private_key = soc.recv(1024).decode()
RSA_private_key = int(RSA_private_key, 16)

decrypted_mssg = De.RSA_OAEP_decrypt(cipher_txt, k0, k1, RSA_modulus, RSA_private_key)

print("\nSent text:")
print(decrypted_mssg)

soc.close()