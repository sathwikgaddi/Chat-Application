# Chat Application using Socket Programming

### Software Required -
1. Python

### Installation Source -

https://www.python.org/downloads/

### Compilation Instructions - 

- Open a Python Shell to run server.py file by using the following command
    ``` python server.py ```
- Open a python shell for each client you want to create by using the following command
    ``` python client.py```
- After successful connection of node to server, 
    1. Enter option 1 to send a message to any other client.
            a. Enter a message to send within the range of 255 bytes.
            b. Enter a Destination Client ID from the active connections to which the message has to be sent.
    2. Enter option 2 to disconnect from the server and exit.


### Files in the Project and their purpose -

#### 1. Server.py :
- Server.py is a python file that instantiates a single server to accept multiple client connections and acts as a hub to send and receive messages.
- #### _Methods in Server.py :_
    **a. _main( )_** - Main method has 2 static values of IP and port number on which the socket is to be created. It creates a socket using socket() method. A new thread is created to listen for new connections. 

    **b. _newConnections( )_** - This functions waits for new Connections on a new thread and allows a new Client to connect to the server unless the clients from 2 to 255 are already full. 
    
    **c. _printAddressTable( )_** - This function prints the address table whenever it is called. The printed address table contains the details of all the active clients that are connected to the server at that point of time.
    
- #### _Classes in Server.py :_
   _**a."Client" -**_
    The Client class is instantiated whenever any new client connection is made and a new thread is created for the instantiated client. Each created instance has the socket and an address that is associated with the items. A new client ID is also created within the range of 2 to 255. 
    The methods inside Client class are -
            **_i. run( ) -_** This function is responsible for accepting the data from the clients and also by sending the received data to the destination to which the frame is destined to. If the method is unable to receive the data, then it assumes that the client is disconnected and removes the client from the connections list. If the message received is not empty or the third field in the frame format is not "ACK" then the message received is forwarded to the destination client which is not as same as the source client.

#### 2. Client.py :
- This file is responsible for creating the clients and handling the client functionalities depending on the input from the users. This files sends and receives the messages through the server and stores the outgoing and incoming data from the client. When this file is executed, a connection to the server will be made and displays the client id to the user.
- #### _Methods in Client.py :_
   After a succesful connection to the server and displaying the client id, the first set of code is responsible to give the user a set of options to either send a message or disconnect from the server. When the user selects to send a message, it prompts the user to type a message and destination client ID. When sending the message, it creates a customized frame format(described below) and sends it to the server by encoding into the bytes.
    **b. _receive( )_** - This function is responsible to receive the data that is sent from the another client through the server. When this method receives a frame from the server, it unpacks the frame and displays the message to the user. This method accepts the data from the server only if that data is destined to this client, else it displays a message saying " Received a data that does not belong here".
    **c. _write_file_input( )_** - This function is responsible to write the message to the client input text. It writes the message that is sent from this client and also stores the destination client ID.
    **d. _write_file_output( )_** - This function is responsible to write the messages to the client output file. It writes the message that is received from other client through the server and also stores the source client ID from which the message is received.

### Frame Format -
- The frame format that is encapsulated to tranfer data between nodes consists of 4 fields in the below format.
- [Source Client ID] [Destination Client ID] [SIZE/ACK] [Message]
- The first field contains the source client ID which is the Id of the node from where the message is sent.
- The second field contains the destination client ID which is the ID of the node to which the message is to be delivered.
- The third field is the SIZE/ACK field, where it has the size of the message. If the size of the message id 0, then the third field will be 'ACK' and the fourth field will be omitted.
- The fourth field is the message field where it contans the message that has to be delivered.






    


 










