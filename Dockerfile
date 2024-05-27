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

# INSTALL NODE
RUN curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt install -y nodejs

# INSTALL NODE DEPENDENCIES
RUN npm i


EXPOSE 9000

ENTRYPOINT ["./entrypoint.sh"]