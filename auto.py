"""
auto mode will help you clean up duplicate files in other folders but keep in main folders.

For example, you have duplicate files:

- c:\photo\1.jpg
- c:\somewhere\1.jpg
- d:\somewhere\1.jpg

You want to keep files in main folder (c:\photo) and cleanup all other files, use this script will save you a day!

  python auto.py

This command will clean up files:

- only if have a copy in main folder
- dup files out of main folder

"""
import logging

from web.app import get_hash_dup, delete_file_by_id

main_folder = r'E:\照片'
process_count = 20000

dup = get_hash_dup(process_count)


def is_in_main_folder(files):
    if len(files) == 1:
        return False

    for f in files:
        file = f[3]
        if file.startswith(main_folder):
            return True
    return False


def cleanup_files(files):
    for f in files:
        file, file_id = f[3], f[0]
        if not file.startswith(main_folder):
            logging.info('delete {}'.format(file))
            try:
                delete_file_by_id(file_id)
            except:
                logging.exception('failed!')
        else:
            logging.info('keep {}'.format(file))


for hash, files in dup.items():
    logging.info('processing {}'.format(hash))
    if is_in_main_folder(files):
        cleanup_files(files)
    else:
        logging.info('No need to cleanup.')

    logging.info('done!\n')
