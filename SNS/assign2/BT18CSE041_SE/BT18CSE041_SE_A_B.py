import socket    
import sys    

import BT18CSE041_SE_A_En as En
import BT18CSE041_SE_A_De as De


soc = socket.socket()        

port = int(sys.argv[1])               
 
soc.connect(('127.0.0.1', port))
print("Connected to server at", port)
 
cipher_txt = soc.recv(1024).decode()

print("\nCipher text:")
print(cipher_txt)

soc.sendall("ACK".encode())

iv = soc.recv(41).decode()

soc.sendall("ACK".encode())

key = soc.recv(41).decode()

decrypted_mssg = De.DES_CBC_decrypt(cipher_txt, key, iv)

print("\nSent text:\n")
print(decrypted_mssg.decode())

soc.close()