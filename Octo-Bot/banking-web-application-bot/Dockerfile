FROM ubuntu:bionic

RUN apt-get update && apt-get install python3 python3-pip wget curl unzip -yf
# Install Chrome
RUN apt-get update -y
RUN apt-get install -y dbus-x11 x11-utils

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
RUN sh -c 'tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/bin/geckodriver'
RUN chmod +x /usr/bin/geckodriver
RUN rm geckodriver-v0.23.0-linux64.tar.gz

USER root
RUN apt update
RUN apt-get install -y poppler-utils
RUN apt-get clean
RUN apt install -y python3 python3-pip firefox
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-xlib python3-tk python3-dev
RUN apt install -y xvfb xserver-xephyr python3-tk python3-dev
RUN Xvfb :99 -ac &
RUN export DISPLAY=:99
RUN pip3 install virtualenv


RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN virtualenv .venv
RUN /bin/bash -c "source .venv/bin/activate"
RUN pip3 install -r requirements.txt
RUN BEZIER_NO_EXTENSION=True pip3 install bezier===2020.2.3
RUN apt-get install -y scrot
COPY . /app
ENTRYPOINT [ "python3", "main.py" ]