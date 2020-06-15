FROM debian:buster-slim

ADD ./bot /

RUN set -e -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get -y upgrade \
    && apt-get -y --no-install-recommends install \
        curl ca-certificates \
#
# install scapy
    && apt-get -y --no-install-recommends install \
       python3-scapy python3-cryptography libwireshark-data \
    && mkdir -p /usr/local/share/wireshark \
    && cp -p /usr/share/wireshark/manuf /usr/local/share/wireshark/ \
    && apt-get -y purge libwireshark-data \
    && ln -s /usr/bin/scapy3 /usr/local/bin/scapy \
    && rm -rf /var/lib/apt/lists/*

VOLUME [ "/root" ]
ENTRYPOINT ["python3", "synflood-attack.py"]