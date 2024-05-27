FROM python:3.12-slim

RUN apt update

RUN apt install -y \
    lsb-release \
    traceroute \
    wget \
    curl \
    iputils-ping \
    bridge-utils \
    dnsutils \
    netcat-openbsd \
    jq \
    redis \
    nmap \
    net-tools \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/bin/portfolio

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["./entrypoint.sh"]