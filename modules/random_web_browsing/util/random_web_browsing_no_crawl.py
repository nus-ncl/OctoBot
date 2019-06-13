dataMeter = 0
goodRequests = 0
badRequests = 0

MAX_DEPTH = 10 #hardcoded for now, change later

SLEEP_MEAN = 10
SLEEP_SD = 3

from util.scrapper import *
import random
import time
import sys
import os

def randomBrowsing(url = "https://ncl.sg", timeAllowed = 1000, \
                maxDepth = MAX_DEPTH, debug = False, sleep = False, \
                onlySameDomain = True):
                
    linkStack = [url]
    
    currDepth = 0
    
    currTime = time.time()
    endTime = currTime + timeAllowed
    
    currUrl = url
    
    blackList = set()
    while (currDepth < maxDepth and time.time() < endTime):
        
        try:
            listOfPages = crawl(url = currUrl, \
                sameDomain = onlySameDomain)
            
            linkStack.append(currUrl)
        except:
            blackList.add(currUrl)
            if (len(linkStack) > 0):
                newUrl = linkStack.pop()
                if (newUrl == currUrl):
                    currUrl = url;
                else:
                    currUrl = newUrl
            else:
                currUrl = url
            continue
        print(listOfPages)
                
        try: #check if listOfPages is non empty
            randomIdx = random.randint(0, len(listOfPages) - 1)
        except:
            print("%s has no other URL to link to, trying the\
                previous URL visited" % currUrl)
            if (len(linkStack) > 0):
                currUrl = linkStack.pop()
            else:
                currUrl = url #go back to the base
                
            continue
                
        randomUrl = listOfPages[randomIdx]
        
        while (randomUrl in blackList):
            if (len(listOfPages) == 1):
                randomUrl = url
                continue
            randomIdx = random.randint(0, len(listOfPages) - 1)
            randomUrl = listOfPages[randomIdx]
            
        currUrl = randomUrl
        print(currUrl)
        
        
        currDepth += 1

           

    
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
    
    parser.add_argument('--debug', type = int, \
            help='Set to 1 for debug output', default = 0)    

    args = parser.parse_args()
    
        
    randomBrowsing(url = args.url, \
                timeAllowed = args.t, \
                maxDepth = args.d, \
                debug = args.debug, \
                noOfInstances = args.i)
    
        
            
            
            
        
