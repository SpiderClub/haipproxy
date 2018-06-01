"""
This module contains the set of haipproxy's exceptions.
"""


class HttpError(Exception):
    """Raise when status code >= 400"""


class DownloadException(Exception):
    """A download error happends when downloading a web page"""
