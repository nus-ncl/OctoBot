FROM python:3.6.9-alpine3.10

# Update apk repo
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories


#Get FireFox pre-requisite drivers (Code referenced from: https://codebug.vip/questions-2020351.htm)
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk
RUN apk add glibc-2.30-r0.apk
RUN apk add glibc-bin-2.30-r0.apk
RUN apk add firefox-esr=60.9.0-r0
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/bin

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install selenium

#COPY files from local directory into container
COPY /main.py /

ADD . /

# Run our web-scraping script
ENTRYPOINT ["python3", "-u", "./main.py"] 
