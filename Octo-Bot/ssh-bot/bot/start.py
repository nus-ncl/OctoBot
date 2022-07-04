#!/usr/bin/python3
import socket
import argparse
import os
import time
import subprocess

loop_script = 'for ((;;)); do sleep 1; echo "hello"; done'

def is_port_used(ip, port):
    """
    check whether the port is used by other program

    :param ip:
    :param port:
    :return: True(in use) False(idle)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


if __name__ == '__main__':
    # "ssh -o StrictHostKeyChecking=no -fNT -L $LOCAL_PORT:$REMOTE_SERVER:$REMOTE_PORT $SSHD_USERNAME@$SSHD_SERVER",

    parser = argparse.ArgumentParser(description="Arguments for program")

    parser.add_argument('--SSHD_USERNAME', type=str, help='SSHD server username')

    parser.add_argument('--SSHD_PORT', type=str, help='SSHD server port', default=22)

    parser.add_argument('--SSHD_PASSWORD', type=str, help='SSHD server password')

    parser.add_argument('--SSHD_SERVER', type=str, help="SSHD server ip")

    parser.add_argument('--REMOTE_SERVER', type=str, help='remote server ip', default='localhost')

    parser.add_argument('--REMOTE_PORT', type=str, help='remote server port', default=22)

    parser.add_argument('--REMOTE_USERNAME', type=str, help='remote server username')

    parser.add_argument('--REMOTE_PASSWORD', type=str, help='remote server password')

    parser.add_argument('--CONCURRENCY', type=int, help='enable/disable ssh concurrency test', default=0)

    parser.add_argument('--UPLOAD', type=int, help='enable/disable ssh upload test', default=0)

    parser.add_argument('--DOWNLOAD', type=int, help='enable/disable ssh download test', default=0)

    args = parser.parse_args()
    if args.REMOTE_PASSWORD is None:
        args.REMOTE_PASSWORD = args.SSHD_PASSWORD
    if args.REMOTE_USERNAME is None:
        args.REMOTE_USERNAME = args.SSHD_USERNAME
    local_addr = '127.0.0.1'
    local_port = 12345
    while (is_port_used(local_addr, local_port)):
        local_port += 1

    # os.environ['LOCAL_PORT'] = str(local_port)
    # UPLOAD = os.getenv('UPLOAD')
    # DOWNLOAD = os.getenv('DOWNLOAD')
    # LOCAL_PORT = os.getenv('LOCAL_PORT')
    # REMOTE_USERNAME = os.getenv('REMOTE_USERNAME')
    # CONCURRENCY = os.getenv('CONCURRENCY')

    # Test Concurrency
    if args.CONCURRENCY == 1:
        print(f"CONCURRENCY enabled")
        # output = subprocess.check_call(f"sshpass -p '{args.SSHD_PASSWORD}' ssh -o StrictHostKeyChecking=no -fNT -p {args.SSHD_PORT} -L {local_port}:{args.REMOTE_SERVER}:{args.REMOTE_PORT} {args.SSHD_USERNAME}@{args.SSHD_SERVER}",stderr=subprocess.STDOUT, shell=True)
        output = subprocess.check_call(f"sshpass -p '{args.SSHD_PASSWORD}' ssh -o StrictHostKeyChecking=no -p {args.SSHD_PORT} {args.SSHD_USERNAME}@{args.SSHD_SERVER} '{loop_script}'",stderr=subprocess.STDOUT, shell=True)

        if output == 0:
            print("Port Forwarded!")

    # Scp Upload
    if args.UPLOAD == 1:
        print(f"UPLOAD enabled")
        # port forwarding
        output = subprocess.check_call(
            f"sshpass -p '{args.SSHD_PASSWORD}' ssh -o StrictHostKeyChecking=no -fNT -p {args.SSHD_PORT} -L {local_port}:{args.REMOTE_SERVER}:{args.REMOTE_PORT} {args.SSHD_USERNAME}@{args.SSHD_SERVER}",
            stderr=subprocess.STDOUT, shell=True)

        if output == 0:
            print("Port Forwarded!")
            os.system(
                f"sshpass -p '{args.REMOTE_PASSWORD}' scp -P {local_port} -o StrictHostKeyChecking=no little_file {args.REMOTE_USERNAME}@localhost:/tmp/little_file" + str(
                    time.time()))

    # Scp Download
    if args.DOWNLOAD == 1:
        print(f"DOWNLOAD enabled")
        # port forwarding
        output = subprocess.check_call(
            f"sshpass -p '{args.SSHD_PASSWORD}' ssh -o StrictHostKeyChecking=no -fNT -p {args.SSHD_PORT} -L {local_port}:{args.REMOTE_SERVER}:{args.REMOTE_PORT} {args.SSHD_USERNAME}@{args.SSHD_SERVER}",
            stderr=subprocess.STDOUT, shell=True)

        if output == 0:
            print("Port Forwarded!")
            os.system(f"sshpass -p '{args.REMOTE_PASSWORD}' scp -P {local_port} -o StrictHostKeyChecking=no -r {args.REMOTE_USERNAME}@localhost:/tmp/downloaded_file ./downloaded_file" + str(time.time()))
            os.system("ls -l .")

    # keep running
    while True:
        # output = subprocess.check_output("nc -zv localhost " + LOCAL_PORT, shell=True)
        # print(output)
        print('running')
        time.sleep(5)
