#!/bin/bash
nohup python3 crawler_booter.py --usage crawler common > crawler.log 2>&1 &
nohup python3 scheduler_booter.py --usage crawler common > crawler_scheduler.log 2>&1 &
nohup python3 squid_update.py --usage https --interval 3 > squid.log 2>&1 &
rm -rf /var/run/squid.pid
squid -N -d1
