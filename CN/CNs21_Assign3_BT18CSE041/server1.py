import socket
import sys
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
    
    except Exception:
        pass

    return str(retval)

# takes in and responds to client's messages
def handleClient(conn, addr):
    connected = True
    while connected:
        # initial message of the length of question being sent
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length != '0':
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            else:
                global client_count
                print(f"Client socket {client_count} sent message: {msg}")
                ans = solve(msg)
                print(f"Sending reply: {ans}")
                conn.send(ans.encode(FORMAT))

        else:
            conn.send("Error: empty message sent to server!".encode(FORMAT))

    conn.close()

# global costants used
SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER_IP,PORT)
HEADER = 64
FORMAT = 'utf-8'

try:
    client_count = 0
    signal.signal(signal.SIGINT, disconnect)

    while True:
        # Creating a socket object where first parameter specifies IPv4 protocol and second parameter specifies TCP protocol
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # for making port reusable in case of program termination on an error
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print("Started Server")
        
        # bind server socket to given address
        server.bind(ADDR)
        server.listen(0)

        # Establish connection with client.
        conn, addr = server.accept()
        client_count += 1
        server.close()

        print(f"Connected with client socket number {client_count}")
        handleClient(conn,addr)


except socket.error as e:
    print("error while assigning PORT ::%s",e)
