#!/usr/bin/python3

"""
Definition of exceptions related to databases
Brings exception handling which
 facilitates debugging
"""

__all__ = [
    "DatabaseException"
]


class LogicException(Exception):
    """
    Exception raised when some error happens on some internal logic
     such as
    """
    pass


class DatabaseException(Exception):
    """
    Base exception to wrap exceptions raised on code related
     to databases
    """

    def __init__(self, msg):
        super(DatabaseException, self).__init__("Database " + msg)


class ProxyException(DatabaseException):
    """
    Exception raised on error present on databases proxy (database.py)
    """

    def __init__(self, msg):
        super(ProxyException, self).__init__("proxy error -> " + msg)


class InternalException(DatabaseException):
    """
    Base exception to wrap for exceptions raised on code
     related to specific databases
    """

    def __init__(self, msg):
        super(InternalException, self).__init__("internal " + msg)


class RelationalDBException(InternalException):
    """
    Exception raised when an error occurs on code related to the relational database
    """

    def __init__(self, msg):
        super(RelationalDBException, self).__init__("relational error -> " + msg)


class TimeSeriesDBException(InternalException):
    """
    Exception raised when an error occurs on code related to the time series database
    """

    def __init__(self, msg):
        super(TimeSeriesDBException, self).__init__("time series error -> " + msg)
