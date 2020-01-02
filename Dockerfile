FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /home/comp_corrector

# install packages
RUN apt-get update -y && apt-get install -y gcc musl-dev libxml2-dev libxslt-dev python-dev python3 python3-pip
# update pip
RUN python3 -m pip install --upgrade pip
# install pipenv
RUN pip3 install pipenv
# install python packages
RUN pipenv install --dev
