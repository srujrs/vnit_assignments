import socket
import sys
from time import sleep
import signal

# signal handling for ctrl + z
def handler(signum, frame):
    pass

# signal handling for ctrl + c
def disconnect(signum, frame):
    global client
    if client:
        client.send(str(len(DISCONNECT_MESSAGE)).encode(FORMAT))
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        sleep(0.5)
    quit()


# global costants used
SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER_IP,PORT)
MSG_SIZE = 1024
FORMAT = 'utf-8'

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

signal.signal(signal.SIGTERM, handler)

try:
    # Establish connection with server
    client.connect(ADDR)

    print("Connected to server")

    signal.signal(signal.SIGINT, disconnect)

    while True:  
        ques = input("Please enter the message to the server: ")

        # send question length initially
        client.send(str(len(ques)).encode(FORMAT))

        # send the question string
        client.send(ques.encode(FORMAT))

        # receive data from the server
        print("Server replied:", (client.recv(MSG_SIZE)).decode(FORMAT))

except socket.error as e:
    print("error while connecting ::",e)
