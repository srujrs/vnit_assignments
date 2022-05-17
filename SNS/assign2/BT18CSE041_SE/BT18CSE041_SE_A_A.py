import socket 
import sys    
import random

import BT18CSE041_SE_A_En as En
import BT18CSE041_SE_A_De as De


soc = socket.socket()        
 
port = int(sys.argv[1])            
 
soc.bind(('', port))        
print ("Socket started at port: %s" %(port))
 
soc.listen()            
 
client, addr = soc.accept()    
print ('Got connection from', addr)

print("\nInput text:\n")

with open('input.txt') as f:
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]
    mssg = "".join(lines)

    print(mssg)

    encrypted_mssg = En.DES_CBC_encrypt(mssg)

    print("\nCipher text:")
    print(encrypted_mssg['ciphertext'])

    client.send(encrypted_mssg['ciphertext'].encode())

    client.recv(3).decode()

    client.send(str(encrypted_mssg['iv']).encode())

    client.recv(3).decode()

    client.send(str(encrypted_mssg['key']).encode())

soc.close()