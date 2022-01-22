import logging
import os
import shutil
import time
import zipfile
import base64

from app.config import settings

from .loader import Loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArchiveLoader(Loader):

    files_folder = f'{settings.MOUNT_FOLDER}/files'
    dataset = []

    def __init__(self):
        logger.info('[ZIP Archive Loader] initialized')
        self.recreate_dataset()

    def recreate_dataset(self):
        self.dataset = []
        try:
            os.mkdir(self.files_folder)
        except:
            pass

        for root, d_names, f_names in os.walk(self.files_folder):
            for f in f_names:
                self.dataset.append(os.path.join(root, f))

    def count(self):
        return len(self.dataset)

    def load_files(self, files, append=False):
        logger.info('Loading files started')

        temp_folder = f'{settings.MOUNT_FOLDER}/temp_files'

        timestamp = time.time()

        output_folder = f'{settings.MOUNT_FOLDER}/files/{timestamp}'

        # prepare temporary folder
        try:
            shutil.rmtree(temp_folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        os.mkdir(temp_folder)

        # prepare file storage
        if append == False:
            try:
                shutil.rmtree(self.files_folder)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        try:
            os.mkdir(self.files_folder)
        except:
            pass

        try:
            os.mkdir(output_folder)
        except:
            pass

        for file in files:
            file_location = f"{temp_folder}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())

        for item in os.listdir(temp_folder):
            if item.endswith('.zip'):
                file_name = f'{temp_folder}/{item}'
                zip_ref = zipfile.ZipFile(file_name)
                zip_ref.extractall(output_folder)
                zip_ref.close()
                os.remove(file_name)

        self.recreate_dataset()

    def load_data(self, page = 0, count = 10):
        offset = page * count
        file_list = self.dataset[offset:offset+count]
        response = []
        for file_name in file_list:
            f = open(file_name, "rb")
            response.append( base64.b64encode(f.read()))
        return response

    def default_process(self):
        pass

    def store(self):
        pass

    def store_to_db(self):
        pass

    def store_to_file(self):
        pass
