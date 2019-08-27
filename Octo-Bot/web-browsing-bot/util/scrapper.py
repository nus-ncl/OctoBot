import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import multiprocessing as mp
import random


import logging
import tldextract as tl
import time
import os, time, sys, re
import requests

import numpy as np

SAME_DOMAIN = True
start_urls = []
allowed_domains = []

DEBUG = 0
agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'   
q = mp.Queue()   

#a truncated normal in range (0, inf) 
def sleepTimeNormal(mean, sd):
    t = -1
    while (t <= 0):
        t = np.random.normal(mean, sd)
    time.sleep(t)

def sleepTimeUnif(start, end):

    t = random.random() * (end - start) + start
    time.sleep(t)


class Crawler(scrapy.Spider):
    name = 'all'
    HTTPCACHE_ENABLED = True
    def __init__(self, startURL):
        self.links=[]
        self.start_urls = startURL
        self.allowed_domains = [getDomain(startURL[0])]
        global q
        global DEBUG
        #q = mp.queue()
        #global collectedLinks
        #collectedLinks.clear()
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'DOWNLOAD_DELAY': 5,
        'HTTPCACHE_ENABLED': True,
        'DEPTH_LEVEL': 5
    }
    
    def parse(self, response):
        
        #print("Existing settings: %s" % self.settings.attributes.keys())
        le = LinkExtractor()
        fromThisIteration = []
        try: 
            le.extract_links(response)
        except:
            raise Exception("dssdsafsfds sds")
        for link in le.extract_links(response):
            if (SAME_DOMAIN and getDomain(link.url) not in self.allowed_domains):
                continue
            try:
                r = requests.get(link.url)
                if (not r.encoding):
                    continue
            except:
                continue
            linkToAppend = re.sub(r";jsessionid=[^?]*", "", link.url)
            fromThisIteration.append(linkToAppend)
            q.put(linkToAppend)
            #print(linkToAppend)
        
        
        
    '''
    def parse(self, response):
        linkToAppend = response.url
        linkToAppend = re.sub(r";jsessionid=[^?]*", "", linkToAppend)
        print(linkToAppend)
        #print(response.css('a::attr(href)'))
        collectedLinks.append(linkToAppend)
        try:
            for href in response.css('a::attr(href)'):
                print(href)
                try:
                    yield response.follow(href, self.parse)
                except:
                    continue
        except:
            pass
    '''    
def getDomain(url):

    extr = tl.extract(url)
    dom = "{}.{}".format(extr.domain,\
                    extr.suffix)
    
    return dom
'''
try:
    from fake_useragent import UserAgent
    ua = UserAgent(cache=False)
    ua.update()
    agent = ua.random
except:
     agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)' 
'''
  
def _getLinksDriver(url, q):
        

    header = {'USER_AGENT': agent}
    process = CrawlerProcess(header)
    process.crawl(Crawler, url)
    
    process.start()
    
    #q.put(collectedLinks.copy())
    
    

def getLinks(url):
    
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)
    global q
    q = mp.Queue() 
    p = mp.Process(target = _getLinksDriver, args = (url, q))
    
    p.start()
    #alternatively,  let terminate time be a function of # links processed 
    p.join(100) #force terminate after a while to prevent excess meemory use, bad solution 
    
    coll = []
    while (not q.empty()):
        coll.append(q.get())
    return coll


def crawl(url, depth = 1, sameDomain = True, sleep_param1 = 10, sleep_param2 = 3, \
        sleepNormal = True):
    
    global SAME_DOMAIN
    SAME_DOMAIN = sameDomain
    
    if (type(url) != list):
        setOfLinks = [url]
    else:
        setOfLinks = url
    
    alreadyProcessed = set()
    
    linksFromLastIteration = [url]
    newLinks = []
    currDepth = 0
    
    currTime = time.time()
    while (currDepth < depth and time.time() < currTime + 40):
        newLinks.clear()
        linksFromLastIteration = [i for i in linksFromLastIteration\
                        if i not in alreadyProcessed]
        #print(linksFromLastIteration)
        if not linksFromLastIteration:
            break
        try:  
            newLinks.extend(getLinks(linksFromLastIteration))
            #reactor.stop()
        except Exception as e:
            raise e
        alreadyProcessed.update(linksFromLastIteration)
        
        newLinks = list(set(newLinks))
        setOfLinks.extend(newLinks)
        
        linksFromLastIteration = newLinks.copy()
        currDepth += 1
        
        if (depth > 1):
            if (sleepNormal):
                sleepTimeNormal(sleep_param1, sleep_param2)
            else:
                a = min(sleep_param1, sleep_param2)
                b = max(sleep_param1, sleep_param2)
                sleepTimeUnif(a, b)
        
    return list(set(setOfLinks))
        