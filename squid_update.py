"""
This module is used to update squid conf periodically.

You can start the task using the following cmd:
python squid_update.py

The default internal value is 10 minutes in settings.py,use
the following cmd if you want a different updating internal
python squid_update.py --internal 5

"""

from scheduler import squid_conf_update


if __name__ == '__main__':
    squid_conf_update()