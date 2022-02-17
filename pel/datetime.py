"""Utils for dates and times."""
import datetime
import time

from pel._vendor.dateutil.parser import parse as dateutil_parse


def str_datetime_to_unixtime(input_str: str) -> float:
    """
    Parse a datetime from a string. Return a UTC Unix timestamp.
    """
    datetime_obj: datetime.datetime = dateutil_parse(input_str)  # type: ignore
    return time.mktime(datetime_obj.timetuple())
