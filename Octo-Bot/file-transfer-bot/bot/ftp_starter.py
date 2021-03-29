import argparse

from ftp_generator import scheduleDownload
from ftp_generator import scheduleUpload


def main():
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="remote ftp_server", required=True,
                        nargs='+', default=None)
    parser.add_argument("-u", help="ftp username", required=True,
                        nargs='+', default=None)
    parser.add_argument("-p", help="ftp password", required=True,
                        nargs='+', default=None)
    parser.add_argument("-t", help="specify your worker", type=int,
                        required=False, nargs='+', default=['1'])
    parser.add_argument("-f",
                        help="specify your function(upload/download)",
                        required=False, nargs='+', default=['download'])
    parser.add_argument("-uf",
                        help="specify your file to be uploaded", required=False,
                        nargs='+', default=['/large_file'])
    parser.add_argument("-df",
                        help="specify your file to be downloaded",
                        required=False, nargs='+', default=['large_file'])

    args = parser.parse_args()

    if args.f[0] == 'upload':
        scheduleUpload(args)
    elif args.f[0] == 'download':
        scheduleDownload(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
