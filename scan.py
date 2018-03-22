import fnmatch
import logging
import os
import sys

import db
from config import *
from utils import setup, md5sum

setup()


def walk_dir(dir_root, action_on_file):
    for sub, dirs, files in os.walk(dir_root):
        for file in files:
            full_path = os.path.join(sub, file)
            action_on_file(full_path)


def count_files(from_dir, pattern="*.*"):
    """count files by pattern in a dir."""
    cache['file_count'] = 0

    def count_action(file):
        if fnmatch.fnmatch(file, pattern):
            cache['file_count'] += 1

    walk_dir(from_dir, count_action)
    return cache['file_count']


def test_count_files():
    logging.info('start...')
    pattern = '*.jpg'
    count = count_files(default_scan_path, pattern)
    logging.info('count of {}: {}'.format(pattern, count))


def save_files_to_db(from_dir, pattern='*.*'):
    """save files by pattern into the db."""
    cache['current'] = 0
    total_count = count_files(from_dir, pattern)
    logging.info('Now scan files({}) from {} ...'.format(pattern, from_dir))
    logging.info('Files found: {}'.format(total_count))

    def save_action(file):
        if fnmatch.fnmatch(file, pattern):
            if db.is_existed(file):
                return

            name = os.path.basename(file).lower()
            hash = md5sum(file)
            db.insert_file(hash, name, file)

            cache['current'] += 1
            if cache['current'] % 2000 == 0:
                logging.info('Processing: {} / {}'.format(cache['current'], total_count))
                db.commit_changes()

    walk_dir(from_dir, save_action)
    db.commit_changes()
    logging.info('Total processing: {} / {}'.format(cache['current'], total_count))


def test_save_files_to_db():
    logging.info('Start...')
    save_files_to_db(default_scan_path, '*.jpg')
    logging.info('Done!')


def delete_file(file_path):
    """delete file from system and mark as deleted in db."""

    if os.path.exists(file_path):
        os.remove(file_path)

    db.mark_deleted(file_path)


def test_delete_file():
    temp_file = os.path.join(default_scan_path, 'temp.temp')
    with open(temp_file, 'w') as f:
        f.write('temp file test')

    save_files_to_db(default_scan_path, '*.temp')
    delete_file(temp_file)

    assert not db.is_existed(temp_file)


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Usage: \n  python scan.py dir1 dir2')

    else:
        dirs_to_scan = sys.argv[1:]

        for dir in dirs_to_scan:
            save_files_to_db(dir, '*.jpg')
