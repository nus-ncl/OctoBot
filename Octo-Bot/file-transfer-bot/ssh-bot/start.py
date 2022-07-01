#!/usr/bin/python3
import socket
import os
import time
import subprocess


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
	local_addr = '127.0.0.1'
	local_port = 12345
	while (is_port_used(local_addr, local_port)):
		local_port += 1

	os.environ['LOCAL_PORT'] = str(local_port)
	UPLOAD = os.getenv('UPLOAD')
	DOWNLOAD = os.getenv('DOWNLOAD')
	LOCAL_PORT = os.getenv('LOCAL_PORT')
	REMOTE_USERNAME = os.getenv('REMOTE_USERNAME')
	CONCURRENCY = os.getenv('CONCURRENCY')

    # Test Concurrency
	if CONCURRENCY == '1':
		output = subprocess.check_call(
			"ssh -o StrictHostKeyChecking=no -fNT -L $LOCAL_PORT:$REMOTE_SERVER:$REMOTE_PORT $SSHD_USERNAME@$SSHD_SERVER",
			stderr=subprocess.STDOUT, shell=True)

		if output == 0:
			print("Port Forwarded!")

	# Scp Upload
	if UPLOAD == '1':
	    # port forwarding
		output = subprocess.check_call(
			"ssh -o StrictHostKeyChecking=no -fNT -L $LOCAL_PORT:$REMOTE_SERVER:$REMOTE_PORT $SSHD_USERNAME@$SSHD_SERVER",
			stderr=subprocess.STDOUT, shell=True)

		if output == 0:
			print("Port Forwarded!")
		    os.system("sshpass -p '$REMOTE_PASSWD' scp -P $LOCAL_PORT -o StrictHostKeyChecking=no little_file $REMOTE_USERNAME@$REMOTE_SERVER:/tmp/little_file" + str(time.time()))

	# Scp Download
	if DOWNLOAD == '1':
	    # port forwarding
		output = subprocess.check_call(
			"ssh -o StrictHostKeyChecking=no -fNT -L $LOCAL_PORT:$REMOTE_SERVER:$REMOTE_PORT $SSHD_USERNAME@$SSHD_SERVER",
			stderr=subprocess.STDOUT, shell=True)

		if output == 0:
			print("Port Forwarded!")
		    os.system("sshpass -p '$REMOTE_PASSWD' scp -P $LOCAL_PORT -o StrictHostKeyChecking=no -r $REMOTE_USERNAME@$REMOTE_SERVER:/tmp/little_file ./little_file" + str(time.time()))
		    os.system("ls -l .")

	# keep running
	while True:
		# output = subprocess.check_output(["nc" ,"-zv" ,"localhost", "$LOCAL_PORT"],shell=True)
		output = subprocess.check_output("nc -zv localhost "+ LOCAL_PORT,shell=True)
		print(output)
		time.sleep(5)
