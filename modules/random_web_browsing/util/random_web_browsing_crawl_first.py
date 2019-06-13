dataMeter = 0
goodRequests = 0
badRequests = 0

MAX_DEPTH = 10 #hardcoded for now, change later
MIN_SLEEP_TIME = 3
MAX_SLEEP_TIME = 5

from util.scrapper import *
import random
#import config
import time
import sys
import os

def crawlThenBrowse(url = "https://ncl.sg", timeAllowed = 1000, \
                maxDepth = 10, onlySameDomain = True, debug = False, \
                sleep = True, noOfInstances = 1, fakeUserAgent = False):
    
    linkStack = [url]
    
    listOfPages = crawl(url, maxDepth, onlySameDomain, debug = debug)   
    
    try:
        listOfPages[0]
    except:
        raise Exception("Base URL has no other links!") 
    
    if debug:
        print(listOfPages)
        
    
    currTime = time.time()
    endTime = currTime + timeAllowed
    nLink = len(listOfPages)
    
    #to support multiple instances easier
    parentPid = os.getpid()
    
    while(noOfInstances > 1 and os.getpid() == parentPid):
        os.fork()
        noOfInstances -= 1
    
    currPid = os.getpid()
    
    
    #if have multiple instances, shouldnt use time as seed
    #since both will start at same time --> same random seq
    #but both will have different PID, so ok
    random.seed(a = currPid)
    while(currTime < endTime):
        
        
        randIdx = random.randint(0, nLink - 1)
        
        randPage = listOfPages[randIdx]
        
        if (debug):
            print("PID = {}, Currrently at {}".format(currPid, randPage))
            print("Time left = {}".format(endTime - time.time()))
        
        if (fakeUserAgent):
            doRequest(randPage, fakeAgent = fakeUAgentHeader)
        else:
            doRequest(randPage)
        
        #sleep a while 
        sleepTime = random.randint(MIN_SLEEP_TIME, MAX_SLEEP_TIME)
        time.sleep(sleepTime)
        
        currTime = time.time()
        
    
    
    
if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(description = \
        "Arguments for program")
    
    parser.add_argument('url', type=str, \
                    help='Target Website')
                    
    parser.add_argument('-t', type = int, \
            help='Time given to crawl website (sec)', default = 1000)
    
    parser.add_argument('-d', type = int, \
            help='How deep to crawl website from entrypoint', default = 3)
            
    parser.add_argument('-i', type = int, \
            help='How many seperate instances to browse website \
            (using forking)', default = 1)          

    parser.add_argument('-s', type = int, \
            help='Set to 0 to allow it to crawl to diff. domain',\
            default = 1)            
    
    parser.add_argument('--sleep', type = int, \
            help='Set to 0 if do not sleep after accessing a website',\
            default = 1)    
    
    parser.add_argument('--debug', type = int, \
            help='Set to 1 for debug output', default = 0)    

    args = parser.parse_args()
    
    crawlThenBrowse(url = args.url, \
                timeAllowed = args.t, \
                maxDepth = args.d, \
                onlySameDomain = args.s, \
                debug = args.debug, \
                noOfInstances = args.i,\
                sleep = args.sleep)
        
            
            
            
        
