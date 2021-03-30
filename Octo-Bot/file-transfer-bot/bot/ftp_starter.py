import argparse
from numpy import random
from time import sleep

from ftp_generator import scheduleDownload
from ftp_generator import scheduleUpload


def main():
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="remote ftp server", required=True,
                        nargs='+', default=None)
    parser.add_argument("-u", help="ftp username", required=True,
                        nargs='+', default=None)
    parser.add_argument("-p", help="ftp password", required=True,
                        nargs='+', default=None)
    parser.add_argument("-s", help="maximum sleep time between download "
                                   "(default 1)", type=int,
                        required=False, nargs='+', default=1)
    parser.add_argument("-t", help="number of thread (default 1)", type=int,
                        required=False, nargs='+', default=1)
    parser.add_argument("-f",
                        help="download function(upload/download)",
                        required=False, nargs='+', default=['download'])
    parser.add_argument("-uf",
                        help="file to be uploaded", required=False,
                        nargs='+', default=['/large_file'])
    parser.add_argument("-df",
                        help="file to be downloaded",
                        required=False, nargs='+', default=['large_file'])

    args = parser.parse_args()

    if args.f[0] == 'upload':
        while True:
            scheduleUpload(args)
            sleep(random.uniform(0, args.s))
    elif args.f[0] == 'download':
        while True:
            scheduleDownload(args)
            sleep(random.uniform(0, args.s))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
