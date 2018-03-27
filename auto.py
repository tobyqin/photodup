import logging

from web.app import get_hash_dup, delete_file_by_id

main_folder = r'E:\照片'
process_count = 1000

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
            delete_file_by_id(file_id)
        else:
            logging.info('keep {}'.format(file))


for hash, files in dup.items():
    logging.info('processing {}'.format(hash))
    if is_in_main_folder(files):
        cleanup_files(files)
    else:
        logging.info('No need to cleanup.')

    logging.info('done!\n')
