import argparse

from ftp_generator import scheduleDownload
from ftp_generator import scheduleUpload


def main():
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="remote ftp_server", required=True,
                        nargs='+', default=None)
    parser.add_argument("--username", help="ftp username", required=True,
                        nargs='+', default=None)
    parser.add_argument("--password", help="ftp password", required=True,
                        nargs='+', default=None)
    parser.add_argument("--worker", help="specify your worker", type=int,
                        required=True, nargs='+', default=None)
    parser.add_argument("--function",
                        help="specify your function(upload/download)",
                        required=True, nargs='+', default=None)
    parser.add_argument("--upload_file",
                        help="specify your file to be uploaded", required=False,
                        nargs='+', default=['/large_file'])
    parser.add_argument("--download_file",
                        help="specify your file to be downloaded",
                        required=False, nargs='+', default=['large_file'])

    args = parser.parse_args()

    if args.function[0] == 'upload':
        scheduleUpload(args)
    elif args.function[0] == 'download':
        scheduleDownload(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
