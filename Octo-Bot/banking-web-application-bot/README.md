# Web-based Banking Application Bot
The bot is specially built for Terracotta web-based banking application.

## Terracotta Banking Application Setup
Detailed information about Terracotta Bank can be found here https://github.com/terracotta-bank/terracotta-bank.git

### Prerequisites
Ensure that the following is installed:

1. Git
2. Java 8

### Download and Run
```
git clone https://github.com/terracotta-bank/terracotta-bank.git
cd terracotta-bank/terracotta-bank-servlet
./gradlew bootRun
```

## Run Terracotta Web Application Bot with Docker
It is recommended to run the bot using Docker container.

### Prerequisites
Ensure that the following is installed:

1. Git
2. Docker ([How to install](https://docs.docker.com/install/))

### Installation
Build

```
git clone https://github.com/nus-ncl/OctoBot.git
cd OctoBot/Octo-Bot/banking-web-application-bot
docker build -t terracotta-bot .
```

Run

```
docker run --network="host" terracotta-bot:latest
```

View All Options
```
docker run --network="host" terracotta-bot:latest -h
usage: main.py [-h] [-url url of application] [-user username]
               [-orgPass password] [-newPass new password]
               [-name name of user] [-email email of user] [-d display]

Arguments for program

optional arguments:
  -h, --help            show this help message and exit
  -url url of application
                        Target Website URL
  -user username        Username to be used
  -orgPass password     Password to be used
  -newPass new password
                        New password to be changed to
  -name name of user    Name to be used
  -email email of user  Email to be used
  -d display            Time to sleep between crawling of website links

```

## Run Terracotta Web Application Bot Natively
If there is a problem to build and run the Bot through Docker, the Bot also can be run natively (without Docker)

### Install Python and its dependencies
Installing git

```
sudo apt update && sudo apt install git
```

Installing pip

```
sudo apt install python3-pip
```

Installing Python dependencies

```
sudo apt-get install python3-tk python3-dev
```

### Install Selenium Web Driver
Install Web driver

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.23.0-linux64.tar.gz
```

Installing Python packages (Selenium, Numpy, ...)

```
pip install selenium==3.141.0 --upgrade cryptography
pip install numpy
pip install pyautogui
pip install bezier
```

### Running the Bot
View all the options

```
git clone https://github.com/nus-ncl/OctoBot.git
cd OctoBot/Octo-Bot/banking-web-application-bot
python3 main.py -d 1
```

