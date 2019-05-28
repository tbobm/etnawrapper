"""
ETNA-related errors.
"""


class MaxRetryError(Exception):
    """Happen when the API stops responding."""

    pass


class BadStatusException(Exception):
    """Receive unexpected reponse code."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)
