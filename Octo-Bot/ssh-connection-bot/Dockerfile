FROM alpine:3.15
ENV DEBIAN_FRONTEND=noninteractive
RUN apk add --no-cache \
  ca-certificates \
  python3 \
  openssh-client \
  ca-certificates \
  bash \
  sshpass 

ADD ./bot /
VOLUME [ "/root" ]
ENTRYPOINT [ "python3", "start.py" ]

