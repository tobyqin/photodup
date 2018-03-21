import hashlib
import logging


def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def setup():
    fmt = '%(asctime)s %(levelname)-8s: %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=fmt,
                        filename='duplicate.log')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(fmt))
    logging.getLogger().addHandler(console)
