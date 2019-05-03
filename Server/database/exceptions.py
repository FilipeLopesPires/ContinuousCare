#!/usr/bin/python3

"""

"""

__all__ = [
    "RelationalDBException",
    "TimeSeriesDBException"
]


class RelationalDBException(Exception):
    """
    Exception raised when an error occurs on code related to the relational database
    """
    pass


class TimeSeriesDBException(Exception):
    """
    Exception raised when an error occurs on code related to the time series database
    """
    pass
