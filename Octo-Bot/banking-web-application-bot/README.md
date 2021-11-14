# Terracotta Bot

## Banking Application Setup
Terracotta Bank: https://github.com/terracotta-bank/terracotta-bank.git

### Prerequisites
Ensure that the following is installed:
1. Java 8

### Setup and Run
```console
git clone https://github.com/terracotta-bank/terracotta-bank.git
cd terracotta-bank/terracotta-bank-servlet
./gradlew bootRun
python3 main.py
```


## Docker Setup

Build
```console
docker build -t terracotta-bot .
```

Run
```console
docker run --network="host" terracotta-bot:latest
```

## VM Setup

## Install Bot Dependencies
Installing git
```console
sudo apt update && sudo apt install git
```

Installing pip
```console
sudo apt install python3-pip
```

Installing other dependencies
```console
sudo apt-get install python3-tk python3-dev
```
Install Web driver
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.23.0-linux64.tar.gz

```

Installing Python packages
```console
pip install selenium==3.141.0 --upgrade cryptography
pip install numpy
pip install pyautogui
pip install bezier
```

## Running the Bot
View all the options
```console
cd OctoBot/Octo-Bot/terracotta-bot
python3 main.py
```