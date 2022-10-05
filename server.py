import socket
import threading
from queue import Queue
import sys

#Variables for holding information about connections and messages
connections = []
total_connections = 2
frame_buffer = Queue()

def printAddressTable():
    print("\n\n")
    print("Address Table:")

    for conn in connections:
        print("Node Id - " + str(conn.id))
        print("Node Info - " + str(conn))
        print("\n")


#Client class
#A new client instance will be created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data_received = self.socket.recv(20480)
                frame_buffer.put(data_received)
                print(str(frame_buffer))
                data_received_in_string = data_received.decode("utf-8")
                received_frame_fields = data_received_in_string.split("][")
                source = int(received_frame_fields[0])
                destination = int(received_frame_fields[1])
                message = received_frame_fields[3]
                flag = received_frame_fields[2]

                print("Received a message '{0}' from {1} to {2}".format(message, str(source), str(destination)))
                
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if message != "" and flag!="ACK":
                for client in connections:
                    if client.id == destination and client.id != self.id:
                        client.socket.sendall(frame_buffer.get())

#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        if(total_connections==255):
            print("255 connections are already in use, Please wait...")
            sys.exit(0)
        else:
            new_client = Client(sock, address, total_connections, "Name", True)
            connections.append(new_client)
            print("connected")
            new_client.socket.sendall(str.encode(str(new_client.id)))
            connections[len(connections) - 1].start()
            print("New connection at ID " + str(connections[len(connections) - 1]))
            total_connections += 1
            printAddressTable()


        
def main():
    #host and port to run the server
    host = '127.0.0.1'
    port = 8080

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print("Waiting for new Connections on a new thread...")
    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()
