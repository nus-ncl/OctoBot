import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import multiprocessing as mp


import logging
import tldextract as tl
import time
import os, time, sys, re

SAME_DOMAIN = True
start_urls = []
allowed_domains = []

DEBUG = 0

q = mp.Queue()   

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
        'DOWNLOAD_DELAY': 0.5,
        'HTTPCACHE_ENABLED': True
        #'DEPTH_LEVEL': 5
    }
    
    def parse(self, response):
        #print("Existing settings: %s" % self.settings.attributes.keys())
        le = LinkExtractor()
        fromThisIteration = []
        for link in le.extract_links(response):
            if (SAME_DOMAIN and getDomain(link.url) not in self.allowed_domains):
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
agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'     
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

def crawl(url, depth, sameDomain = True):
    
    global SAME_DOMAIN
    SAME_DOMAIN = sameDomain
    
    setOfLinks = [url]
    
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
        
    return list(set(setOfLinks))
        