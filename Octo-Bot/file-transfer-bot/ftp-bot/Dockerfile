#FROM debian:buster-slim
FROM python:3

ADD ./bot /

RUN set -e -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get -y upgrade \
    && apt-get -y --no-install-recommends install \
        curl ca-certificates \
# generate 900M dummy file
    # && dd if=/dev/zero of=/tmp/large_file bs=1024 count=921600 \
    # && dd if=/dev/zero bs=1024 count=921600 of=/tmp/large_file \
# install scapy
    && apt-get -y --no-install-recommends install \
       python3-scapy python3-cryptography libwireshark-data \
    && mkdir -p /usr/local/share/wireshark \
    && cp -p /usr/share/wireshark/manuf /usr/local/share/wireshark/ \
    && apt-get -y purge libwireshark-data \
    && ln -s /usr/bin/scapy3 /usr/local/bin/scapy \
    && rm -rf /var/lib/apt/lists/*

VOLUME [ "/root" ]
ENTRYPOINT ["python3", "ftp_starter.py"]
