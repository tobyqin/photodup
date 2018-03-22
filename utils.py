import hashlib
import logging

from config import cache


def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def setup():
    if 'setup' not in cache:
        fmt = '%(asctime)s %(levelname)-8s: %(message)s'
        logging.basicConfig(level=logging.DEBUG,
                            format=fmt,
                            filename='photo.log')

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(fmt))
        logging.getLogger().addHandler(console)
        cache['setup'] = True
