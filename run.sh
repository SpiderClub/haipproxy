#!/usr/bin/env bash
python crawler_booter.py --usage crawler &
python crawler_booter.py --usage validator &
python scheduler_booter.py --usage crawler &
python scheduler_booter.py --usage validator &
python squid_update.py