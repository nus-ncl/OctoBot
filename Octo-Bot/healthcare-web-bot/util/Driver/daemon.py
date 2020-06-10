import time 
import threading
import time

""" Runs the bot in daemon mode

daemonActions specifies the actions that the bot should make while in daemon mode
daemonMode specifies the logic for the bot in daemon mode
"""
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