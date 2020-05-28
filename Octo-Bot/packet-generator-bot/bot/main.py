import argparse

from os import system

# Internal Imports
from utils.RandNetParamsGen import *
from ReplayGenerator import *


def main():

    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--interactive', help="use scapy interactive console", dest='interactive', action='store_true')
    parser.add_argument("-a", "--src", help="(optional) specify source ip", required=False, default=GenerateRandomIp())
    parser.add_argument("-A", "--dst", help="(optional) specify destination ip", required=False, default=GenerateRandomIp() )
    parser.add_argument("-p", "--sport", help="(optional) specify source port", type=int, required=False, default=RandomSafePortGenerator())
    parser.add_argument("-P", "--dport", help="(optional) specify destination port", type=int, required=False, default=RandomSafePortGenerator())
    parser.add_argument("-m", "--smac", help="(optional) specify source mac", required=False, default=GenerateRandomMac())
    parser.add_argument("-M", "--dmac", help="(optional) specify destination mac", required=False, default=GenerateRandomMac())
    parser.add_argument("-i", "--interface", help="(optional) specify interface", required=False, default='eth0')
    parser.add_argument("-r", "--pcap", help="pcap base to (r)eplay", required=False, action='append',default=[])
    parser.add_argument("-o", "--outfile", help="(optional) output packet capture file", required=False, default=None)
    parser.add_argument("-t", "--time", help="(optional) continuously generate traffic for a set duration of time", required=False, default=None)
    parser.add_argument("-l", "--loop", help="(optional) number of times to loop", type=int, required=False, default=1)
    parser.add_argument("-d", "--delay", help="(optional) delay between each loop", required=False, default="0")

    args = parser.parse_args()

    #Use Scapy Interactive Console
    if args.interactive:
        system("scapy")
    
    # Modules switching (extensible)
    if args.pcap is not []:
        generateReplay(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
