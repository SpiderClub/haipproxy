#!/bin/bash
nohup python crawler_booter.py --usage crawler common > crawler.log 2>&1 &
nohup python scheduler_booter.py --usage crawler common > crawler_scheduler.log 2>&1 &
nohup python crawler_booter.py --usage validator init > init_validator.log 2>&1 &
nohup python crawler_booter.py --usage validator https > https_validator.log 2>&1&
nohup python scheduler_booter.py --usage validator https > validator_scheduler.log 2>&1 &
nohup python squid_update.py --usage https --interval 3 > squid.log 2>&1 &
rm -rf /var/run/squid.pid
squid -N -d1
