import logging
import os
import shutil
import time
import zipfile
import base64

from app.config import settings
from fastapi.responses import FileResponse, Response

from .loader import Loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArchiveLoader(Loader):

    files_folder = f'{settings.MOUNT_FOLDER}/files'

    def __init__(self, config):
        logger.info('[ZIP Archive Loader] initialized')        

    def get_dataset(self):
        data = []
        try:
            os.mkdir(self.files_folder)
        except:
            pass
        for root, d_names, f_names in os.walk(self.files_folder):
            for f in f_names:
                data.append(os.path.join(root, f))

        return data

    def count(self):
        return len(self.get_dataset())

    def clean(self):
        try:
            shutil.rmtree(self.files_folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def load_content(self, content, format, append):
        return self.load(content, append)

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
            self.clean()

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

    def load_data(self, page=0, count=10, format=''):
        resp = None

        data = self.get_dataset()

        if format == 'application/json':
            offset = page * count
            file_list = data[offset:offset+count]
            resp = []
            for file_name in file_list:
                f = open(file_name, "rb")
                filename = file_name.split("/")[-1]
                resp.append({
                    "name": filename,
                    "base64encoded": base64.b64encode(f.read())}
                )
        elif format == 'application/zip':
            resp = 'ZIP format not implemented'
        else:
            resp = FileResponse(
                data[page], filename=data[page].split("/")[-1])
        
        return resp

    def looad_from_store(self):
        # return path names so far
        return self.get_dataset()

    def default_process(self):
        pass

    def store(self):
        pass

    
    def export_content_types(self):
        return [
            'application/zip',
            'application/binary',
            'application/json'
        ]
