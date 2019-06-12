import socket
import time
import os

host = 'localhost' 

clients = {} #dict clientName:(ip, port)
client_ip = set() #for fast keep track of existing client 
port = 5000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Using <a class="zem_slink" title="User Datagram Protocol" href="http://en.wikipedia.org/wiki/User_Datagram_Protocol" rel="wikipedia">UDP</a> protocol
serverSocket.bind((host,port))
serverSocket.setblocking(1)

quitting = False
print("Server Started.")
while not quitting:
    try:
        
        data, addr = serverSocket.recvfrom(1024) # Here, 1024 is the buffer, which can be set to any value
    except:
        raise Exception("Communication error")
        
    if "Quit" in str(data):
        quitting = True
            
        #if not an existing client    
    if addr not in client_ip:
        client_ip.add(addr)
        clientName = data.decode()
        clients[clientName] = addr
        print("Added clientname: {} with ip, port {}".\
        format(clientName, str(clients[clientName])))
        continue;
            

    print("recv = " + data.decode())
    print(str(addr))
        
    #parse data
        
    #split into list by space
    decoded_data = data.decode().split()
    
    #if master issued command, parse it
    issuer = decoded_data[0]
    if (issuer == "MASTER"):
        print("sdsdfsdfdsf")
        pid = os.fork()
        #for child process
        if (pid == 0):
            print("pfsdnkf")
            clientName = decoded_data[1]
            print(clientName)
            #do something, talk to client
            clientIp = clients.get(clientName)
            if (clientIp != None):
                pass
            else:
                raise Exception("Client with name {} not found".\
                format(clientName))
                
            try:
                commands = decoded_data[2:]
                
            except:
                raise Exception("Invalid Syntax")
            try:
                commandsToSend = " ".join(commands)
                
                commandsAsBytes = str.encode(commandsToSend)
                serverSocket.sendto(commandsAsBytes, clientIp)
                print(commandsAsBytes)
            
            except:
                raise Exception("Error sending command {}".\
                format(commandsToSend))
            
            
            os.kill(os.getpid(), 0) #kill myself after finishing 
            
        
        #no need to wait for child, go on to keep listening
    
    #print(time.ctime(time.time()) + str(addr) + ": :" + str(data)) # Printing <a class="zem_slink" title="Timestamp" href="http://en.wikipedia.org/wiki/Timestamp" rel="wikipedia">Time stamp</a> of messages from each client.
    '''
    for client in clients:
        serverSocket.sendto(data, client) '''

serverSocket.close()
