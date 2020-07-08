# Octobot: Healthcare web browsing activity bot

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
joelczk@OctoBot:~$ cd OctoBot/Octo-Bot/<bot-name>
joelczk@OctoBot:~$OctoBot/Octo-Bot/<bot-name>$ git clone https://github.com/joelczk/OctoBot.git
joelczk@OctoBot:~$OctoBot/Octo-Bot/<bot-name>$ sudo chmod 777 run.sh
joelczk@OctoBot:~$OctoBot/Octo-Bot/<bot-name>$ ./run.sh
```

Check the running container:

```console
joelczk@OctoBot:~/OctoBot$ sudo docker ps -a
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS                   PORTS               NAMES
acfcdc3f568f        web-crawler:latest   "python -u ./main.py…"   2 days ago          Exited (0) 2 days ago                        priceless_bhaskara
```

Access the data scraped :

```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ sudo docker cp <container name>:/data <directory>
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ sudo chmod -R <directory>
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ cd <directory>/data
```

## Usage
Here is the help page for the healthcare-web-bot program:
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -h
usage: main.py [-h] [-t time] [-r role] [-b bot] [-u username] [-p password] [-m daemon | no-daemon]
Arguments for program

optional arguments:
  -h, --help   show this help message and exit
  -t time      Time to sleep between crawling of website links
  -r role      Role that the bot should login as
  -b bot       Number of bots for the choosen role
  -u username  Username to be used for login
  -p password  Password to be used for login
  -m [daemon | no-daemon]
```

## Examples

### Crawl with waiting time in between website links
This allows the bot to crawl website links with a specified sleep time between crawling. The default value is set to 0, if this is not specified
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -t 20
```

### Crawl the website with a specified role
This allows the bot to crawl the website using an intended role. The roles available are "admin", "patient", "researcher" and "therapist". The bot will take on the default role of an admin if this is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -r admin
```

### Crawl the website with multiple bots in parallel
Specify the number of parallel bots that are to be run at the same time. The default value is set to 1 if this field is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -b 5
```

### Crawl the bot with specified username and password
Specify the username and password to login and crawl the website. The bot will login from the csv list of usernames and passwords if this is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -u <usernam> -p <password>
```
### Execute the bot in a daemon mode
The bot will start to execute in daemon mode and start to run in the background in another thread. This argument is optional and should only be specified if the user wants to run the bot in daemon mode.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-web-bot -m daemon
```

Detailed Documentations can be found at [DOCS](Docs/README.md)
