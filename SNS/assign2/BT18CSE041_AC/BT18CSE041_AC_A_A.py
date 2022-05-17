import socket 
import sys    
import random

import BT18CSE041_AC_A_En as En
import BT18CSE041_AC_A_De as De


soc = socket.socket()        
 
port = int(sys.argv[1])            
 
soc.bind(('', port))        
print ("Socket started at port: %s" %(port))
 
soc.listen()            
 
client, addr = soc.accept()    
print ('Got connection from', addr)

print("\nInput text:")

with open('input.txt') as f:
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]
    mssg = "".join(lines)

    print(mssg)

    encrypted_mssg = En.RSA_OAEP_encrypt(mssg)

    print("\nCipher hex:")
    print(hex(encrypted_mssg['cipher']))

    client.send(str(hex(encrypted_mssg['cipher'])[2:]).encode())

    client.recv(3).decode()

    client.send(str(hex(encrypted_mssg['k0'])[2:]).encode())

    print("\nLength of r:")
    print(hex(encrypted_mssg['k0']))

    client.recv(3).decode()

    client.send(str(hex(encrypted_mssg['k1'])[2:]).encode())

    print("\nPadded length:")
    print(hex(encrypted_mssg['k1']))

    client.recv(3).decode()

    client.send(str(hex(encrypted_mssg['RSA modulus'])[2:]).encode())

    print("\nRSA modulus:")
    print(hex(encrypted_mssg['RSA modulus']))

    client.recv(3).decode()

    client.send(str(hex(encrypted_mssg['RSA private key'])[2:]).encode())

    print("\nRSA private key:")
    print(hex(encrypted_mssg['RSA private key']))

soc.close()