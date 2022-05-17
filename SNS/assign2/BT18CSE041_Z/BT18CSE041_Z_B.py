import socket    
import sys     

import BT18CSE041_Z_En as En 
import BT18CSE041_Z_De as De


soc = socket.socket()        

port = int(sys.argv[1])               
 
soc.connect(('127.0.0.1', port))
print("Connected to server at", port)

cipher_txt = soc.recv(2048).decode()

print("\nCipher text:")
print(cipher_txt)

soc.sendall("ACK".encode())

R1_key = soc.recv((len(cipher_txt)//2)*8).decode()
R2_key = soc.recv((len(cipher_txt)//2)*8).decode()

decrypted_mssg = De.decrypt(cipher_txt, R1_key, R2_key)

print("\nSent text:")
print(decrypted_mssg)

soc.close()