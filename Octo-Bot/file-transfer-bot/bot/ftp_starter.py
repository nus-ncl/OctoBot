import argparse
import random
import time

from ftp_generator import scheduleDownload
from ftp_generator import scheduleUpload


def main():
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", metavar='server', help="remote ftp server", required=True, nargs='+',
                          default=None)
    parser.add_argument("-u", metavar = 'username', help="ftp username", required=True, nargs='+',
                          default=None)
    parser.add_argument("-p", metavar = 'password', help="ftp password", required=True, nargs='+',
                          default=None)
    parser.add_argument("-d", metavar='delay', help="maximum sleep time between download (default 1)", type=int, required=False,
                            default=1)
    parser.add_argument("-t", metavar = 'thread', help="number of thread (default 1)", type=int,required=False,
                            default=1)
    parser.add_argument("-f", metavar = 'function',required=False, nargs='+',
                        help="download function(upload/download)",
                            default=['download'])
    parser.add_argument("-uf", metavar = 'uploaded_file',
                        help="file to be uploaded",  required=False,
                          default=['/large_file'])
    parser.add_argument("-df", metavar = 'downloaded_file',required=False,
                        help="file to be downloaded",default=['large_file'])

    args = parser.parse_args()

    if args.f[0] == 'upload':
        while True:
            scheduleUpload(args)
            time.sleep(random.uniform(0, args.d))
    elif args.f[0] == 'download':
        while True:
            scheduleDownload(args)
            time.sleep(random.uniform(0, args.d))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
