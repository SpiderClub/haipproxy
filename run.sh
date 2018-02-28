#!/usr/bin/env bash
python crawler_booter.py --usage crawler common ajax &
python scheduler_booter.py --usage crawler common ajax &
python crawler_booter.py --usage validator init &
python crawler_booter.py --usage validator https &
python scheduler_booter.py --usage validator https &
python squid_update.py --usage https --internal 3 &