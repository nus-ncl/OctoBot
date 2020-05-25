# Web Crawling Bot

## Introduction
This bot is specially developed for crawling the webpages and automating user actions of the development server for NUSMed website.

## Prerequisites
Ensure that the following is installed
1. Docker ([How to install](https://docs.docker.com/install/ "https://docs.docker.com/install/"))
2. Git

## Installation
Installing git:
```console
joelczk@OctoBot:~$ sudo apt update && sudo apt install git
```

Build and Run Docker image
```console
joelczk@OctoBot:~$ git clone https://github.com/joelczk/OctoBot.git
joelczk@OctoBot:~$ cd OctoBot/
joelczk@OctoBot:~$ sudo chmod 777 run.sh
joelczk@OctoBot:~/OctoBot$ ./run.sh
```

Check the running container:

```console
joelczk@OctoBot:~/OctoBot$ sudo docker ps -a
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS                   PORTS               NAMES
acfcdc3f568f        web-crawler:latest   "python -u ./main.py…"   2 days ago          Exited (0) 2 days ago                        priceless_bhaskara
```

Access the data scraped :

```console
joelczk@OctoBot:~/OctoBot$ sudo docker cp <container name>:/data <directory>
joelczk@OctoBot:~/OctoBot$ sudo chmod -R <directory>
joelczk@OctoBot:~/OctoBot$ cd <directory>/data
```
Detailed Documentations can be found at [DOCS](https://github.com/joelczk/web-crawler/blob/master/Docs/README.md)
