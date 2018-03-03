import os
import logging
from logging import config as log_conf


__all__ = [
    'crawler_logger', 'scheduler_logger',
    'client_logger', 'other_logger'
]

log_dir = os.path.dirname(os.path.dirname(__file__))+'/logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_path = os.path.join(log_dir, 'haiproxy.log')

log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'scheduler_logger': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'client_logger': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'other_logger': {
            'handlers': ['file'],
            'level': 'info',
        }
    }
}

log_conf.dictConfig(log_config)

crawler_logger = logging.getLogger('cralwer')
scheduler_logger = logging.getLogger('validator')
client_logger = logging.getLogger('client')
other_logger = logging.getLogger('other')