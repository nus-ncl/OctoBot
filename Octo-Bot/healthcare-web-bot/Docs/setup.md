## Setting-up
This section explains how to set up the dependencies for executing the bot

Ensure that the following are set-up properly:
1. Docker
2. Git

### Using Git
You need to have Git to clone this repositories onto your desired directory.

Installing git:
```console
joelczk@OctoBot:~$ sudo apt update && sudo apt install git
```

### Using Docker
To use docker container to run the bot, you need to install `docker`. On Ubuntu, `docker` can be installed with the following commands:
```console
joelczk@OctoBot:~$ sudo apt-get update
joelczk@OctoBot:~$ sudo apt-get install docker-ce docker-ce-cli containerd.io
joelczk@OctoBot:~$ sudo docker run hello-world
```

For other distributions, visit [here](https://docs.docker.com/engine/install/)

You can then build the docker image using the provided script like this:
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~$chmod 755 build.sh
joelczk@OctoBot/Octo-Bot/<bot-name>:~$./build.sh 
```

Finally you can run the bot with `docker run`. Here is an example:
```console
joelczk@OctoBot/Octo-Bot/<bot-name>:~$ docker run healthcare-web-bot:latest [-t time] [-r role] [-b bot] [-u username] [-p password] [-m mode of execution]
```
You can refer [here](Usage.md) for more information of the arguments for running the bot
