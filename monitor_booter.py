"""
This module is used to start prometheus exporter.

If you have your own metrics to monitor, just custom them
in haipproxy.monitor.exporter
"""
from haipproxy.monitor import exporter_start


if __name__ == '__main__':
    exporter_start()