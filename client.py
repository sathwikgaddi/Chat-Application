import socket
import threading
import sys

my_id = ""


def write_file_output (message, f):
    filename = "node{id}_output.txt".format(id = my_id)
    with open(filename, "ab") as text_file:
        text_file.write(str.encode(str(f) + ": "))
        text_file.write(message)
        text_file.write('\n'.encode())

def write_file_input (message, to):
    filename = "node{id}_input.txt".format(id = my_id)
    with open(filename, "ab") as text_file:
        text_file.write(str.encode(str(to) + ": "))
        text_file.write(message)
        text_file.write('\n'.encode())

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string


def receive(socket, signal):
    while signal:
        try:
            print("listening")
            data_received = socket.recv(1024)
            data_received_in_str = data_received.decode("utf-8")
            received_frame_fields = data_received_in_str.split("][")
            # print(received_frame_fields)
            message = received_frame_fields[3]
            source = received_frame_fields[0]
            destination = int(received_frame_fields[1])
            if(destination == my_id):
                print("Message from {0} : {1}".format(str(source), message))
                print("\n")
                # print("Enter a message to send")
                write_file_output(str.encode(message), source)
                
            else:
                print("Received a data that does not belong here")

        except:
            print("You have been disconnected from the server")
            signal = False
            break

#Get host and port
host = '127.0.0.1'
port = 8080

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    my_id = sock.recv(1024)
    my_id = int(my_id.decode("utf-8"))
    print("\n")
    print("Successfully created a new Node with ID {0}".format(str(my_id)))
    print("\n")
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()



    #Send data to server
    #str.encode is used to turn the string message into bytes so it can be sent across the network
while True:
    source = my_id
    option = 0
    while(True):
        print("")
        print("Enter an option from below to proceed: ")
        print("1. Send Message")
        print("2. Disconnect to server and exit")
        option = int(input(""))
        if(option == 1 or option == 2):
            break
        print("Please enter a valid option!!")
    if(option == 2):
        print("You are disconnected from the server")
        sys.exit(0)
    message = ""
    while True:
        print("\n")
        message = input("Enter a message to send: ")
        if(len(str.encode(message))>255):
            print("Message size exceeded, Please enter a valid message size!!")
        else:
            break

    destination = int(input("Enter destination ClientID: "))
    size = len(str.encode(message))
    if(size>0):
        frame_to_send = str(source) + "][" + str(destination) + "][" + str(size) + "][" + message
    else:
        frame_to_send = str(source) + "][" + str(destination) + "][" + "ACK"
    #print(frame_to_send)

    write_file_input(str.encode(message), destination)
    
    sock.sendall(str.encode(frame_to_send))

    
