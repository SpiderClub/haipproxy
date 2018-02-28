#!/usr/bin/env bash
nohup python crawler_booter.py --usage crawler common > crawler.log 2>&1 &
nohup python scheduler_booter.py --usage crawler common > crawler_scheduler.log 2>&1 &
nohup python crawler_booter.py --usage validator init > init_validator.log 2>&1 &
nohup python crawler_booter.py --usage validator https > https_validator.log 2>&1&
nohup python scheduler_booter.py --usage validator https > validator_scheduler.log 2>&1 &
python squid_update.py --usage https --internal 3