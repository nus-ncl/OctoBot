FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y \
  ca-certificates \
  python3 \
  openssh-server \
  netcat \
  sshpass \
#  iproute2 \
#  ipppd \
#  expect \
#  wget \
  && apt-get clean -q && apt-get autoremove --purge \
  && rm -rf /var/lib/apt/lists/*

#WORKDIR /root

# Copy files
# COPY id_rsa .ssh/id_rsa
#COPY little_file little_file
#COPY start.py start.py

# RUN chmod 0400 .ssh/id_rsa

ADD ./bot /
VOLUME [ "/root" ]
ENTRYPOINT [ "python3", "start.py" ]

