dataMeter = 0
goodRequests = 0
badRequests = 0

MAX_DEPTH = 10 #hardcoded for now, change later
MIN_SLEEP_TIME = 3
MAX_SLEEP_TIME = 5

from util.scrapper import *
import random
import time
import requests
import sys

def crawlThenBrowse(url = "https://ncl.sg", timeAllowed = 1000, \
                maxDepth = 2, onlySameDomain = True, debug = False, \
                sleep = True):
    
    linkStack = [url]
    
    try:
        listOfPages = crawl(url, maxDepth, onlySameDomain)
    except:
        sys.exit("Error in Crawling URL")

    try:
        listOfPages[0]
    except:
        raise Exception("Base URL has no other links!") 
    
    if debug:
        print(listOfPages)
        
    
    currTime = time.time()
    endTime = currTime + timeAllowed
    nLink = len(listOfPages)
    
    while(currTime < endTime):
        
        
        randIdx = random.randint(0, nLink - 1)
        
        randPage = listOfPages[randIdx]
        
        r = requests.get(randPage)
        if (debug):
            print("Currrently at {}".format(randPage))
            print("Time left = {}".format(endTime - time.time()))

        
        
        #sleep a while 
        sleepTime = random.randint(MIN_SLEEP_TIME, MAX_SLEEP_TIME)
        time.sleep(sleepTime)
        
        currTime = time.time()
        
    
    
    