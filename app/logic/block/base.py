from enum import Enum
from typing import List

from app.configuration.settings import Settings
from app.generic_components.generic_types.error import ErrorNotImplemented
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.loader.base import BlockLoader
from app.logic.block.loader.file import BlockLoaderFile
from app.logic.block.storage.base import BlockStorage
from app.logic.block.storage.memory import BlockStorageMemory


class BlockType(str, Enum):
    base = "base"
    csv_loader = "csv_loader"


class BlockBase:

    def __init__(self, name="",
                 block_type=BlockType.base,
                 loader=BlockLoaderFile(),
                 storage: BlockStorage = BlockStorageMemory()):
        super().__init__()

        self.log = LogBase.log(self.__class__.__name__)
        self.__settings = Settings()
        self.__name = name
        if len(name) == 0:
            self.__name = self.__settings.block_name
        self.__type = block_type
        self.log.debug("Initialized block {}".format(self.__name))
        self.__loader = loader
        self.__storage = storage

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def itemize(self, data):
        yield data

    def filter(self, item):
        return True

    def train(self):
        raise ErrorNotImplemented()

    def save_model(self, model):
        raise ErrorNotImplemented()

    def load_model(self):
        raise ErrorNotImplemented()

    @property
    def storage(self):
        return self.__storage

    def clear_storage(self):
        self.__storage.clear()

    @property
    def loader(self):
        return self.__loader

    def load_data(self, from_scratch=False):
        raise ErrorNotImplemented()

    def count(self):
        raise ErrorNotImplemented()
