import socket
import threading
import time
 
tLock = threading.Lock()
shutdown = False
 
def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data))
        except:
            pass
        finally:
            tLock.release()
 
host = '127.0.0.1'
port = 10000
 
server = ('127.0.0.1',5000)
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
 
rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()
 
alias = "MASTER"

#send name to server
s.sendto(str.encode(alias), server)
message = input(alias + " ")
#msg format: first word is name, then subsequently commands seperated by space
while message != 'q':
    if message != '':
        s.sendto(bytes(alias + " " + message, 'utf-8'), server)
    tLock.acquire()
    message = input(alias + " ")
    tLock.release()
    time.sleep(0.2)
 
shutdown = True
rT.join()
s.close()
