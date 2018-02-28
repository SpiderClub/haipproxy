FROM ubuntu:16.04

MAINTAINER ResolveWang <resolvewang@foxmail.com>

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN apt update
RUN apt install squid -yq
RUN sed -i 's/http_access deny all/http_access allow all/g' /etc/squid/squid.conf
RUN service squid start
RUN cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
RUN apt install python3 python3-pip -yq
RUN which python3|xargs -i ln -s {} /usr/bin/python
RUN which pip3|xargs -i ln -s {} /usr/bin/pip
COPY . /haipproxy
WORKDIR /haipproxy
RUN pip install -i https://pypi.douban.com/simple/ -r requirements.txt
CMD ['python', 'crawler_booter.py', '--usage', 'crawler', 'common']