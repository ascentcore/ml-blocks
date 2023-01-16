import base64
import os
import time

from starlette.responses import FileResponse

from app.configuration.settings import Settings
from app.generic_components.file_wrapper.file_wrapper import WrapperFile
from app.generic_components.folder_wrapper.folder_wrapper import FolderWrapper
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.loader.base import BlockLoader


class LoaderFileInject:
    __name: str = None
    __content = None
    __extension: str = None

    def __init__(self, filename, file_extension, content):
        self.log = LogBase.log(self.__class__.__name__)
        self.__name = filename
        self.__content = content
        self.__extension = file_extension

    @property
    def name(self):
        return self.__name

    @property
    def extension(self):
        return self.__extension

    @property
    def content(self):
        return self.__content


class LoaderFileInjectDict(LoaderFileInject):

    def __init__(self, data):
        self.log = LogBase.log(self.__class__.__name__)
        self.__data = data
        super().__init__(self.load_data())

    def load_data(self):
        file_name, file_extension = os.path.splitext(self.__data['filename'])
        content = self.__data['content']
        return file_name, file_extension, content


class LoaderFileInjectFile(LoaderFileInject):

    def __init__(self, data):
        self.log = LogBase.log(self.__class__.__name__)
        self.__data = data
        super().__init__(self.load_data())

    def load_data(self):
        file_name, file_extension = os.path.splitext(self.__data.filename)
        content = self.__data.file.read()
        return file_name, file_extension, content


class BlockLoaderFile(BlockLoader):

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(self.__class__.__name__)
        self.__settings = Settings()
        self.__folder_path = f'{self.__settings.mount_folder}/{self.__settings.storage_folder}'
        self.log.info(f'Storage folder {self.__folder_path} {self.__settings.mount_folder}')
        self.__dataset = []
        self.initialize()

    @property
    def data_folder(self):
        return self.__folder_path

    @property
    def dataset(self):
        return self.__dataset

    def initialize(self):
        FolderWrapper.create_folder(path=self.data_folder)
        self.refresh()

    def refresh(self):
        self.__dataset = WrapperFile.get_all_files_from_folder(path=self.data_folder,
                                                               extensions=[".csv"])  # TODO is it ok?
        self.log.info('Refreshed dataset {}'.format(self.count()))

    def count(self):
        return len(self.dataset)

    def query(self, page=0, count=100, format='raw'):
        offset = page * count
        file_list = self.dataset[offset:offset + count]
        return file_list

    # def query(self, page=0, count=100, format='application/file'):
    #     offset = page * count
    #     file_list = self.dataset[offset:offset + count]
    #     if format == 'application/file':
    #         file_name = self.dataset[page]
    #         yield file_name
    #         # yield FileResponse(file_name, headers={
    #         #     'Content-Disposition': f'filename="{WrapperFile.get_filename(file_name)}"'})
    #     else:
    #         for file in file_list:
    #             if format is None or format == 'raw':
    #                 yield WrapperFile.read_content(path=file)
    #             elif format == 'application/json' or format == 'application/json+base64':
    #                 content = WrapperFile.read_content(path=file, flags="rb")
    #                 filename = WrapperFile.get_filename(path=file)
    #                 yield \
    #                     {
    #                         "name": filename,
    #                         "base64encoded": base64.b64encode(
    #                             content) if format == 'application/json+base64' else content
    #                     }

    def file_location(self, filename, extension):
        return f"{self.__folder_path}/{filename}-{int(time.time())}{extension}"

    def inject_content(self, data: LoaderFileInject):
        file_location = self.file_location(filename=data.name, extension=data.extension)
        WrapperFile.write_to_file(path=file_location, lines=data.content)
        self.log.info('Injected new data {}'.format(file_location))
        self.refresh()
        return file_location

    def entries(self, format='application/file'):
        for item in self.query(0, self.count(), format):
            yield item
