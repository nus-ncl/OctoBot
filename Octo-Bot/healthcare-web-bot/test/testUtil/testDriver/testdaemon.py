import time 
import threading
import time

def daemonActions():
    while(True):
        time.sleep(2)

def daemonMode():
    while(True):
        thread = threading.Thread(target = daemonActions, args = ())
        thread.daemon = True
        thread.start()
        time.sleep(1)
        thread.join()