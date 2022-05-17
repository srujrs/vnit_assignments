import socket 
import sys    

import BT18CSE041_Z_En as En 
import BT18CSE041_Z_De as De


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

    encrypted_mssg = En.encrypt(mssg)

    print("\nCipher text:")
    print(encrypted_mssg['ciphertext'])

    client.send(encrypted_mssg['ciphertext'].encode())

    client.recv(3).decode()

    # print("\nRound1 key =", encrypted_mssg['R1_key'], ", Round2 key =", encrypted_mssg['R2_key'])

    client.send(str(encrypted_mssg['R1_key']).encode())
    client.send(str(encrypted_mssg['R2_key']).encode())

soc.close()