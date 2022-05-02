import logging
import time
import shutil
import os
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)


class FileLoader:

    def __init__(self, settings):
        self.mount_folder = settings.MOUNT_FOLDER
        self.storage_folder = f'{settings.MOUNT_FOLDER}/data/file_loader_files'
        self.create_folder()

    def create_folder(self):
        try:
            logger.info(
                f'Trying to create file loader location {self.storage_folder}')
            os.mkdir(self.storage_folder)
        except FileExistsError:
            pass

    def initialize(self, *args):
        self.dataset = []
        for root, _, f_names in os.walk(self.storage_folder):
            for f in f_names:
                self.dataset.append(os.path.join(root, f))

        logger.info(f'Dataset initialized with value {self.dataset}')
        self.dataset = self.process_fn(self, self.dataset) 
        return self.dataset

    def count(self):
        return len(self.dataset)

    def clean(self):
        try:
            shutil.rmtree(self.storage_folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        self.create_folder()
        self.dataset = []

    def load_content(self, file, *args):
        file_name, file_extension = os.path.splitext(file.filename)
        file_location = f"{self.storage_folder}/{file_name}-{int(time.time())}{file_extension}"

        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        logger.info(f'Appending to loader dataset: {file_location}')
        if self.process_fn([file_location]):
            self.dataset.append(file_location)
        return file_location

    def query(self, page=0, count=100, format='application/json'):
        if format is None or format == 'application/json':
            offset = page * count
            file_list = self.dataset[offset:offset+count]
            resp = []
            for file_name in file_list:
                f = open(file_name, "rb")
                filename = file_name.split("/")[-1]
                resp.append({
                    "name": filename,
                    "base64encoded": f.read()}
                )

            return resp
        else:
            raise Exception('FileLoader supports only "application/json"')
