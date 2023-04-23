from datetime import datetime
import time
import os


import os
from time import time
from datetime import datetime


def current_timestamp():
    """
    Returns the current UTC date and time in timestamp format.
    :return: datetime
    """
    timestamp = datetime.utcnow()
    return timestamp


def current_unix_time():
    """
    Returns the current UTC date and time in UnixTime format.
    :return: int
    """
    unix_time = int(time())
    return unix_time


def get_size(start_path):
    """
    Returns the size of the given directory.
    :param start_path: string
    :return: int
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

