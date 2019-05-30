FROM debian:stretch

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-tk && \
    ln -s $(which python3) /usr/bin/python && \
    ln -s $(which pip3) /usr/bin/pip

RUN python -m pip install --upgrade pip && python -m pip install jupyter

WORKDIR /pyolin
COPY . /pyolin

CMD python -m pip install -r requirements.txt ; python -m jupyter notebook --ip 0.0.0.0 --allow-root --no-browser