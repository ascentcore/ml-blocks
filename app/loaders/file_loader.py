import logging
import time
import os
import base64

from fastapi.responses import FileResponse

from app.settings import initialize_folder
from .base_loader import BaseLoader

logger = logging.getLogger(__name__)


class FileLoader(BaseLoader):    

    def __init__(self, settings):
        self.mount_folder = settings.MOUNT_FOLDER
        self.storage_folder = 'file_loader_files'
        self.current_hash = None
        self.initialize()

        logger.info(
            f'File loader initialized {self.storage_folder}. Number of existing files: {self.count()}')

    def initialize(self):
        initialize_folder(self.storage_folder)
        self.refresh()

    def refresh(self):
        self.dataset = []
        for root, _, f_names in os.walk(f'{self.mount_folder}/{self.storage_folder}'):
            for f in f_names:
                self.dataset.append(os.path.join(root, f))
        
        logger.info(f'Refreshed file loader dataset. {len(self.dataset)}')


    def count(self):
        return len(self.dataset)    

    def load_content(self, file, *args):
        write_type = 'wb+'
        if isinstance(file, dict):
            write_type = 'w'
            file_name, file_extension = os.path.splitext(file['filename'])
            content = file['content']
        else:
            file_name, file_extension = os.path.splitext(file.filename)
            content = file.file.read()

        file_location = f"{self.storage_folder}/{file_name}-{int(time.time())}{file_extension}"

        with open(file_location, write_type) as file_object:
            file_object.write(content)

        logger.info(f'Appending to loader dataset: {file_location}')
        self.dataset.append(file_location)
        return file_location

    def formats(self):
        return ['raw', 'application/json', 'application/json+base64', 'application/file']

    def entries(self, format = None):
        for item in self.query(0, self.count(), format):
            yield item
    
    def query(self, page=0, count=100, format='raw'):
        offset = page * count
        return self.dataset[offset:offset+count]

    def _query(self, page=0, count=100, format='raw'):
        offset = page * count
        file_list = self.dataset[offset:offset+count]
        if format is None or format == 'raw':
            for file in file_list:
                with open(file) as file_object:
                    yield file_object.read()
        elif format == 'application/json' or format == 'application/json+base64':
            for file_name in file_list:
                f = open(file_name, "rb")
                filename = file_name.split("/")[-1]
                yield {
                    "name": filename,
                    "base64encoded":  base64.b64encode(f.read()) if format == 'application/json+base64' else f.read()
                }
        elif format == 'application/file':
            file_name = self.dataset[page]
            yield FileResponse(file_name,  headers={
                                    'Content-Disposition': f'filename="{os.path.basename(file_name)}"'})
        else:
            raise Exception('FileLoader supports only "application/json"')
