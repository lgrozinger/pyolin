FROM debian:buster

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-tk && \
    ln -s $(which python3) /usr/bin/python && \
    ln -s $(which pip3) /usr/bin/pip

RUN python -m pip install --upgrade pip && \
    python -m pip install jupyter \
                          pandas \
                          scipy \
                          matplotlib \
                          similaritymeasures \
                          seaborn \
                          requests

RUN apt-get install -y gnuplot \
                       texlive-base \
                       texlive-fonts-recommended \
                       imagemagick

WORKDIR /pyolin
