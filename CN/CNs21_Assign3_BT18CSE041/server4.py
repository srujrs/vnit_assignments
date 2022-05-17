import socket
import sys
import select
import signal


# signal handling for ctrl + z
def disconnect(signum, frame):
    quit()

def getActualMsg(msg):
    num = len(msg)
    extra = len(str(num))
    power = 1

    while 10**power < num:
        power += 1
    if 10**power == num:
        return extra - 1
    else:
        return extra


# global costants used
SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER_IP,PORT)
HEADER = 64
MSG_SIZE = 1024
FORMAT = 'utf-8'

# Creating a socket object where first parameter specifies IPv4 protocol and second parameter specifies TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# for making port reusable in case of program termination on an error
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Started Server")

signal.signal(signal.SIGINT, disconnect)

try:

    # bind server socket to given address
    server.bind(ADDR)
    server.listen(5)

    input = [server]

    while True:
        inputready,outputready,exceptready = select.select(input,[],[])

        for s in inputready:

            if s == server:
                # handle the server socket
                client, address = server.accept()
                input.append(client)

            else:
                # handle all other sockets
                msg = s.recv(MSG_SIZE).decode(FORMAT)

                # client disconnected so remove it from list
                if msg == '11' + DISCONNECT_MESSAGE:
                    s.close()
                    input.remove(s)

                else:
                    # send back the data received
                    toSend = msg[getActualMsg(msg):len(msg)]

                    print(f"Client socket sent message: {toSend}")
                    print(f"Sending reply: {toSend}")

                    # echo back data received
                    s.send(toSend.encode(FORMAT))

except socket.error as e:
    print("error while assigning PORT ::%s",e)
