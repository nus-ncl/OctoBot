# Octo-Bot: Healthcare automatic registration bot

## Introduction
This bot is specially developed for automating creation user accounts for development server of NUSMed website

## Installation
This section explains how to install the dependencies for executing the bot

Ensure that the following are set-up properly:
1. Docker
2. Git

### Using Git
You need to have Git to clone this repositories onto your desired directory.

Installing git:
```console
joelczk@OctoBot:~$ sudo apt update && sudo apt install git
joelczk@OctoBot:~$ git clone https://github.com/nus-ncl/OctoBot.git
```

### Using Docker
To use Docker container to run the bot, you need to install `Docker`. On Ubuntu, `Docker` can be installed with the following commands:
```console
joelczk@OctoBot:~$ sudo apt-get update
joelczk@OctoBot:~$ sudo apt-get install docker-ce docker-ce-cli containerd.io
joelczk@OctoBot:~$ sudo docker run hello-world
```

For other distributions, visit [here](https://docs.docker.com/engine/install/). It is not recommended to use Docker using `Windows` OS.

You can then build the Docker image using the provided script like this:
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~$chmod 755 build.sh
joelczk@OctoBot/Octo-Bot/<bot-name>:~$./build.sh 
```

Finally you can run the bot with `docker run`. Here is an example:
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~$ docker run healthcare-registration-bot:latest [-u hostname]
```

## Developing the bot

Create a local build of the Docker image:

```console
joelczk@OctoBot:~$ cd OctoBot/Octo-Bot/<bot-name>
joelczk@OctoBot/Octo-Bot/<bot-name>:~/OctoBot$ docker build . -t healthcare-registration-bot:latest
```

Check the local image:

```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker images
REPOSITORY                     TAG                 IMAGE ID            CREATED             SIZE
healthcare-registration-bot    latest              f112835c8a07        1 days ago          1.1GB
python                         3.8-alpine3.10      02d2bb146b3b        2 weeks ago         918MB
```
Run the Docker image:

```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~/OctoBot$ docker run healthcare-registration-bot -u <url>
```

Check the running container:

```console
joelczk@OctoBot:~/OctoBot$ sudo docker ps -a
CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS                     PORTS               NAMES
7b57f44bbba0        healthcare-registration-bot:latest   "python3 -u ./main.py"   13 seconds ago      Exited (1) 3 seconds ago                       suspicious_germain
```

## Flowchart of program flow

![Program flow](https://github.com/joelczk/OctoBot/blob/master/Octo-Bot/healthcare-registration-bot/images/programflow.png)

## Usage
Here is the help page for the healthcare-registration-bot program:
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-registration-bot -h
usage: main.py [-h] [-u hostname]

Arguments for program

optional arguments:
  -h, --help   show this help message and exit
  -u hostname  URL of the website that the bot is using
```

## Examples

## Specify hostname for bot to crawl
This specifies the hostname that the bot is crawling. The default hostname is `https://10.10.0.112/` if it is not specified.
```console
joelczk@OctoBot:~/OctoBot/Octo-Bot/<bot-name>$ docker run healthcare-registration-bot -u https://10.10.0.112/
```

## Configuration
There are a total of 3 files that should be modified --> `admin.csv`, `patient.csv` and `therapist.csv`

Here is an example format of `admin.csv` file:
```csv
<username>, <password>
```

Here is an example format of `patient.csv` file:
```csv
<username>, <password>,<diagnosis code>
```

Here is an example format of `patient.csv` file:
```csv
<username>, <dob(yyyy-mm-dd)>, <first name>, <last name>, <address>, <email>, <postal code>, <contact number>, <password>, <Field to be automated(height/weight/temp/bp)>, <data of field to be automated>
```

## Tests
There are 2 types of tests that can be run for `healthcare-registration-bot`, namely tests with Firefox interface UI and tests without Firefox interface UI

### Running tests with Firefox interface UI (It requires a desktop terminal)
```console
joelczk@OctoBot/Octo-Bot/<bot-name>/test:~/OctoBot$ python3 TestUI.py
```

### Running tests without Firefox interface UI (It does not require a desktop terminal)
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~/OctoBot$ python3 TestNoUI.py
```

By default, `test.sh` file runs both tests with and without Firefox interface UI (It requires a desktop terminal for this)