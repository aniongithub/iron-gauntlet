FROM balenalib/raspberry-pi:stretch

# Update sources and install some basics
RUN apt-get update &&\
    apt-get install -y \
    wget \
    nano

# Install Python 3.6.8, needed for fauxmo
RUN apt-get install -y \
    build-essential \
    tk-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline6-dev \
    libdb5.3-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libssl-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    zlib1g-dev \
    libffi-dev &&\
    cd /tmp &&\
    wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz &&\
    tar zxf Python-3.6.8.tgz &&\
    cd Python-3.6.8 &&\
    ./configure &&\
    make -j 4 &&\
    make install &&\
    # Make it the default
    ln -sfn $(which python3.6) $(which python3)

# Install wirinpi for testing
RUN apt=get install -y \
    wirinpi

# Install our dependencies
RUN python3.6 -m pip install --upgrade pip setuptools wheel &&\
    python3.6 -m pip install RPi.GPIO &&\
    python3.6 -m pip install numpy &&\
    python3.6 -m pip install fauxmo

WORKDIR /usr/local/src/iron-gauntlet/
COPY * /usr/local/src/iron-gauntlet/

CMD [ "fauxmo", "-c", "IronGauntlet.json", "-v" ]