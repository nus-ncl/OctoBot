dataMeter = 0
goodRequests = 0
badRequests = 0

MAX_DEPTH = 10 #hardcoded for now, change later

SLEEP_MEAN = 10
SLEEP_SD = 3

from .scrapper import *
import random
import time
import sys
import os

def randomBrowsing(url = "https://ncl.sg", timeAllowed = 1000, \
                maxDepth = MAX_DEPTH, debug = False, sleep = True, \
                onlySameDomain = True):
                
    linkStack = [url]
    
    currDepth = 0
    
    currTime = time.time()
    endTime = currTime + timeAllowed
    
    currUrl = url
    
    blackList = set()
    while (currDepth < maxDepth and time.time() < endTime):
        
        goBack = False
        try:
            listOfPages = crawl(url = currUrl, \
                sameDomain = onlySameDomain)
            if (len(listOfPages) > 1):
                linkStack.append(currUrl)
            else:
                goBack = True 
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
        
        if (goBack):
            currUrl = linkStack.pop()
        else:
            currUrl = randomUrl
        print(currUrl)
        
        
        currDepth += 1

           