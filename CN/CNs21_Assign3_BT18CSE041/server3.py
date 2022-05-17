import socket
import sys
import select
import signal


# signal handling for ctrl + z
def disconnect(signum, frame):
    quit()

# checks for operands and operator validitiy and sends answer
def solve(ques):
    retval = "Please enter Integers!"
    try:
        operators = ques.split()
        op1 = int(operators[0])
        op2 = int(operators[2])
        
        if operators[1] == '+':
            retval = int(op1) + int(op2)
        elif operators[1] == '-':
            retval = int(op1) - int(op2)
        elif operators[1] == '*':
            retval = int(op1) * int(op2)
        elif operators[1] == '/':
            retval = int(op1) / int(op2)
        else:
            retval = "Error: Invalid Operator!"
    
    except ValueError:
        pass

    return str(retval)


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
                msg_length = s.recv(HEADER).decode(FORMAT)

                if msg_length == '11' + DISCONNECT_MESSAGE:
                    s.close()
                    input.remove(s)

                elif msg_length != '0':
                    msg_length = int(msg_length)
                    msg = s.recv(msg_length).decode(FORMAT)

                    if msg == DISCONNECT_MESSAGE:
                        s.close()
                        input.remove(s)

                    else:
                        print(f"Client socket sent message: {msg}")
                        
                        ans = solve(msg)
                        print(f"Sending reply: {ans}")

                        s.send(ans.encode(FORMAT))

                else:
                    s.send("Error: empty message sent to server!".encode(FORMAT))

except socket.error as e:
    print("error while assigning PORT ::%s",e)
