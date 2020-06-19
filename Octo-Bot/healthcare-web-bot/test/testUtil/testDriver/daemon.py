import time 
import threading
import time

def daemonActions():
    
    '''
    Actions that the bot is going to take while in daemon mode

    Arguments:
        None
    
    Returns:
        None
    '''
    while(True):
        time.sleep(2)

def daemonMode():

    '''
    The main logic behind executing the bot in daemon mode

    Arguments:
        None

    Returns:
        None
    '''
    while(True):
        thread = threading.Thread(target = daemonActions, args = ())
        thread.daemon = True
        thread.start()
        time.sleep(1)
        thread.join()
        