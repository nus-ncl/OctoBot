## Octo-Bot Preparation and Developer Guide

In order to understand how each independent bot is developed and built,
please check each of the type of bot documentation below:

1. [Generic web browsing bot using Python Scrapy](web-browsing-bot/README.md)
2. [Javascript-enabled web browsing bot using Java Selenium](javascript-web-bot/README.md)
3. [Customized web browsing bot for Healthcare environment using Python Selenium](healthcare-web-bot/README.md)
4. [Customized registration bot for Healthcare environment using Python Selenium](healthcare-web-bot/README.md)
5. [Packet generator bot for generating realistic traffic using Python Scapy](packet-generator-bot/README.md)
6. [TCP Sync attack bot for simulating DDoS using Python Scapy](synflood-attack-bot/README.md)
7. [File Transfer using SSH Protocol](file-transfer-bot/README.md)
8. [Customized web browsing for banking web application](banking-web-application-bot/README.md)

All the bots are also publish in [DockerHub](https://hub.docker.com/repositories/nusncl1/) to be pulled easier from the 
orchestrator. 

But in order to setup automatic build in the DockerHub when there is any changes 
in the master branch of the Github repository, please follow this steps:
- Create repository in the Dockerhub with the same as in the Github
- In the `Builds Settings` section please check and do these sub-steps:

  - Status Github Repository should be `Connected`
  - Choose the name of repository name
  - Add `BUILD RULES` by clicking `+` character
  - Source Type `Branch`, Source `master`, Docker Tag `latest`, Dockerfile location `Octo-Bot/<botname>/`
  - Click `Create and Build`

- Check the status in `Build Activity` and make sure the status is `Success`. It will take sometime depending on the size of the Docker image.