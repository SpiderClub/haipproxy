FROM ubuntu:16.04

MAINTAINER ResolveWang <resolvewang@foxmail.com>

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    ' > /etc/apt/sources.list

RUN apt update
RUN apt install squid -yq && service squid start && cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
RUN apt install python3 python3-pip -yq
RUN which python3|xargs -i ln -s {} /usr/bin/python
RUN which pip3|xargs -i ln -s {} /usr/bin/pip
COPY . /haipproxy
WORKDIR /haipproxy
RUN pip install -i https://pypi.douban.com/simple/ -r requirements.txt
CMD ['python', 'crawler_booter.py', '--usage', 'crawler']
