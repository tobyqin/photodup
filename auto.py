"""
auto mode will help you clean up duplicate files in other folders but keep in main folders.

For example, you have duplicate files:

- c:\photo\1.jpg
- c:\somewhere\1.jpg
- d:\somewhere\1.jpg

when: main_is_keep = True:
    This script will keep files in main folder (c:\photo) and cleanup all other files.

when: main_is_keep = False:
    This script will delete files in main folder and keep all other files.

Script Usage:
  python auto.py

The clean up rules:

- when keep main, clear all duplicates out of main.
- when clear main, clear all duplicates in main.

"""
import logging

from web.app import get_hash_dup, delete_file_by_id

main_folder = r'H:\Photos\TODO'
process_count = 20000
main_is_keep = False

dup = get_hash_dup(process_count)


def dup_in_main_folder(files):
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
        should_delete = file.startswith(main_folder) != main_is_keep

        if should_delete:
            logging.info('delete {}'.format(file))
            try:
                delete_file_by_id(file_id)
            except:
                logging.exception('failed!')
        else:
            logging.info('keep {}'.format(file))


for hash, files in dup.items():
    logging.info('processing {}'.format(hash))
    if dup_in_main_folder(files):
        cleanup_files(files)
    else:
        logging.info('No need to cleanup.')

    logging.info('done!\n')
