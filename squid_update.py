"""
This module is used to update squid conf periodically.

If you belong to admin group, you can start the task using the following cmd:
python squid_update.py

The default usage value is 'https' and interval value is 5 minutes,
use the following cmd if you want a different usage and updating interval
sudo python squid_update.py --usage weibo --interval 6

Notice that if you don't belong to admin group, you must run this script with sudo:
sudo python squid_update.py
"""

from haipproxy.scheduler import squid_conf_update


if __name__ == '__main__':
    squid_conf_update()
