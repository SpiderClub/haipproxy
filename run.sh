#!/usr/bin/env bash
python crawler_booter.py --usage crawler common ajax &
python crawler_booter.py --usage validator init https &
python scheduler_booter.py --usage crawler common ajax &
python scheduler_booter.py --usage validator https &
python squid_update.py