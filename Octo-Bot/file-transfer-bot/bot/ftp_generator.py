from threading import Thread
import time
import os
import ftplib


def scheduleUpload(args):
    jobs = []
    for i in range(1, args.worker[0] + 1):
        params = {
            'server': args.server[0],
            'username': args.username[0],
            'password': args.password[0],
            'upload_file': args.upload_file[0]
        }

        jobs.append(Thread(target=doUpload(params),
                           name=(f"Upload #{i}")))

        print(f"Upload #{i} is running")

    print(f"Starting all {len(jobs)} Upload(s)....")
    for job in jobs:  # Start all job threads
        job.start()


def scheduleDownload(args):
    jobs = []
    for i in range(1, args.worker[0] + 1):
        params = {
            'server': args.server[0],
            'username': args.username[0],
            'password': args.password[0],
            'download_file': args.download_file[0]
        }

        jobs.append(Thread(target=doDownload(params),
                           name=f"Download #{i}"))

        print(f"Download #{i} is running")

    print(f"Starting all {len(jobs)} download(s)....")
    for job in jobs:  # Start all job threads
        job.start()


def doUpload(params):
    filename = params['upload_file']
    ftp_server = params['server']
    username = params['username']
    password = params['password']
    fileSavedAs = "large_file"
    suffix = str(time.time())
    ftpCommand = "STOR %s" % filename.split('/')[-1] + '_' + suffix

    session = ftplib.FTP(ftp_server, user=username, passwd=password)
    file = open(filename, 'rb')
    print("Upload from:")
    print(filename)
    print("Saving to:")

    session.storbinary(ftpCommand, file)
    file.close()
    session.quit()


def doDownload(params):
    filename = params['download_file']
    ftp_server = params['server']
    username = params['username']
    password = params['password']
    fileSavedAs = "large_file"
    ftpCommand = "RETR %s" % filename;

    session = ftplib.FTP(ftp_server, user=username, passwd=password)
    print("Download from:")
    print(params['server'] + ':' + filename)
    print("Saving to:")
    print(
        os.path.dirname(os.path.abspath(__file__)) + '/' + filename.split('/')[
            -1])
    # download
    file = open(filename.split('/')[-1], 'wb')
    session.retrbinary(ftpCommand, file.write)
    file.close()
    session.quit()
