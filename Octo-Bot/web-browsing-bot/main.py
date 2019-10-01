import argparse
import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = \
        "Arguments for program")
    

    parser.add_argument('u', type=str, \
                    help='Target Website URL')
    
    parser.add_argument('c', type = int, \
            help = "1 for crawl before browsing, 0 (default) otherwise",
            default = 0)

    parser.add_argument('-t', type = int, \
            help='Time given to crawl website (sec)', default = 1000)

    parser.add_argument('-d', type = int, \
            help='How deep to crawl website from entrypoint', default = 3)


    parser.add_argument('-s', type = int, \
            help='Set to 0 to allow it to crawl to diff. domain',\
            default = 1)

    parser.add_argument('--debug', type = int, \
            help='Set to 1 for debug output', default = 0)

    args = parser.parse_args()
    
    if (args.c == 1):
        from util.random_web_browsing_crawl_first import *
        crawlThenBrowse(url = args.u, \
                timeAllowed = args.t, \
                maxDepth = args.d, \
                onlySameDomain = args.s, \
                debug = args.debug)
        
                
    elif (args.c == 0):
        from util.random_web_browsing_no_crawl import *
        randomBrowsing(url = args.u, \
                timeAllowed = args.t, \
                maxDepth = args.d, \
                debug = args.debug)
                
    else:
        raise Exception ("Invalid argument for -c")
