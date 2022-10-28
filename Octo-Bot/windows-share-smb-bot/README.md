# Octo-Bot: Windows SMB Bot for sharing file

## Introduction
This bot is specially developed for automating sharing file (download or upload) with Windows OS using SMB Protocol.

## Prerequisites
Ensure that the following is installed
1. Docker ([How to install](https://docs.docker.com/install/ "https://docs.docker.com/install/"))
2. Git

## Installation
Installing git:
```console
$ sudo apt update && sudo apt install git
```

Build and Run Docker image
```console
$ cd OctoBot/Octo-Bot/windows-share-smb-bot
$ docker build . -t windows-share-smb-bot:latest
$ docker run windows-share-smb-bot:latest -u <windows_user> -p <windows_password> -c <bot_name> -s <smb_server_name> -i <smb_server_ip> -d <windows_domain> -r <remote_file> -l <local_file>
.
..
File-in-linux.txt
File-in-windows.txt
File-in-windows.txt is downloaded in the current local directory
File-in-linux.txt is uploaded in remote shared directory
```

Check the running container:

```console
$ docker ps -a

CONTAINER ID   IMAGE                          COMMAND                  CREATED         STATUS         PORTS                       NAMES
d7b46a052c39   windows-share-smb-bot:latest   "python -u ./main.py…"   5 seconds ago   Up 5 seconds                               recursing_vaughan

```