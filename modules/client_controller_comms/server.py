import socket
import time

host = '127.0.0.1' # <a class="zem_slink" title="Localhost" href="http://en.wikipedia.org/wiki/Localhost" rel="wikipedia">Loopback address</a> for the port
port = 5000 # Port assigned after the range of reserved ports i.e. 1025

clients = [] # Now clients can be many, so this list maintains the clients.

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Using <a class="zem_slink" title="User Datagram Protocol" href="http://en.wikipedia.org/wiki/User_Datagram_Protocol" rel="wikipedia">UDP</a> protocol
serverSocket.bind((host,port))
serverSocket.setblocking(0)

quitting = False
print("Server Started.")
while not quitting:
    try:
        data, addr = serverSocket.recvfrom(1024) # Here, 1024 is the buffer, which can be set to any value
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)

        print("recv = " + data.decode())
        print(str(addr))
            
        print(time.ctime(time.time()) + str(addr) + ": :" + str(data)) # Printing <a class="zem_slink" title="Timestamp" href="http://en.wikipedia.org/wiki/Timestamp" rel="wikipedia">Time stamp</a> of messages from each client.
        for client in clients:
            serverSocket.sendto(data, client)
    except:
        pass
serverSocket.close()
