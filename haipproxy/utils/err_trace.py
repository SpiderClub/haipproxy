from raven import Client

from ..config.settings import SENTRY_DSN

__all__ = ['client']

client = Client(SENTRY_DSN)
