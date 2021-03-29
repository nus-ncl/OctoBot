import argparse
import threading

from os import system
from ftp_generator import scheduleDownload
from ftp_generator import scheduleUpload

def main():


    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="remote ftp_server", required=True, nargs='+',default=None)
    parser.add_argument("--username", help="ftp username", required=True, nargs='+', default=None)
    parser.add_argument("--password", help="ftp password", required=True, nargs='+',default=None )
    parser.add_argument("--worker", help="specify your worker", type=int, required=True, nargs='+',default=None )
    parser.add_argument("--function", help="specify your function(upload/download)", required=True, nargs='+',default=None )
    parser.add_argument("--upload_file", help="specify your file to be uploaded", required=False, nargs='+',default=['/large_file'] )
    parser.add_argument("--download_file", help="specify your file to be downloaded", required=False, nargs='+',default=['large_file'] )
    # parser.add_argument("-p", "--target-port", help=" specify target port", type=int, required=True, nargs='+', default=None)
    args = parser.parse_args()
    # print(type(args.filename[0]))
    # print(type(args.url[0]))
    # print(type(args.token[0]))
    # print(type(args.worker[0]))
    if args.function[0] == 'upload':
        scheduleUpload(args)
    elif args.function[0] == 'download':
        scheduleDownload(args)
    else:
        parser.print_help()

    # # Use Scapy Interactive Console
    # if args.interactive:
    #     system("scapy")
    #
    # if args.target is not None and args.target_port is not None:
    #     scheduleSynFlood(args)
    # else:
    #     parser.print_help()

if __name__ == '__main__':
    main()
