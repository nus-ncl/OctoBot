# Octo-Bot: File Transfer Bot

## Introduction
This bot is specially developed for automating file transfer (download and upload) using FTP protocol.

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
$ cd OctoBot/Octo-Bot/file-transfer-bot
$ docker build . -t file-transfer-bot:latest
$ docker run file-transfer-bot:latest -s <server_ip> -u <ftp_user> -p <ftp_password>
```

Check the running container:

```console
$ docker ps -a

CONTAINER ID        IMAGE                          COMMAND                  CREATED              STATUS                          PORTS               NAMES
b72b0bf9e8c7        file-transfer-bot:latest       "python3 ftp_start..."   About a minute ago   Exited (0) About a minute ago                       nifty_northcutt
```


## Usage
Here is the help page for the complete usage of the bot program:
```console
$ docker run file-transfer-bot:latest
  usage: ftp_starter.py [-h] -s SERVER -u USERNAME --p PASSWORD 
                        [-d TIME (Second)] [-t THREAD -f FUNCTION]
                        [-uf UPLOAD_FILE] [-df DOWNLOAD_FILE]
```
