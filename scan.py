import logging
from pathlib import *

from config import *
from utils import setup

setup()


def count_files(dir_path, pattern="*.*"):
    """count file by pattern in a path."""
    p, count = Path(dir_path), 0

    for f in p.glob(pattern="**/" + pattern):
        count += 1

    return count


def test_count_files():
    logging.info('start...')
    count = count_files(default_scan_path, '*.jpg')
    logging.info('count of jpg: {}'.format(count))
