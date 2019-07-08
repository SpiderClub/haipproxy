#!/bin/bash
nohup python3 runspiders.py -o proxy > crawler.log 2>&1 &
nohup python3 runspiders.py --usage crawler common > crawler_scheduler.log 2>&1 &
nohup python3 runclient.py -s 30 > squid.log 2>&1 &
rm -rf /var/run/squid.pid
squid -N -d1
