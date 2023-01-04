import os
import shutil
import time
import random


def prepare_folder(folder, cleanup=False):
    if cleanup:
        try:
            shutil.rmtree(folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    try:
        os.makedirs(folder)
    except OSError as e:
        print("Warning: %s - %s." % (e.filename, e.strerror))


def prepare_local_files(cleanup=False,  suffix='', prefix='stores/tests', count=300):

    prepare_folder(f'{prefix}/file_loader_files', cleanup=cleanup)

    with open(f'{prefix}/file_loader_files/tmp_{suffix}.csv', 'w') as file:
        file.write('time,col1,col2,col3\n')
        for i in range(0, count):
            file.write(
                f'{time.ctime(time.time())},{random.random()},{random.random()},{random.random()}\n')
