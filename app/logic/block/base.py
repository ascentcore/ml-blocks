from enum import Enum

import app.block.types
import app.logic.block.types
from app.configuration.settings import Settings
from app.generic_components.generic_types.error import ErrorNotImplemented
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.plugin_loader.plugin_loader import PluginLoader
from app.logic.block.loader.base import BlockLoader
from app.logic.block.storage.base import BlockStorage

# where to search for extensions
BlockSources = [app.block.types.__file__, app.logic.block.types.__file__]


class BlockBase:
    """Basic resource class. Concrete resources will inherit from this one
    """
    plugins = []

    # For every class that inherits from the current,
    # the class name will be added to plugins
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if type(cls) not in cls.plugins:
            cls.plugins.append(cls)

    def __init__(self,
                 name="BlockSimple",
                 loader=BlockLoader(),
                 storage=BlockStorage()):
        super().__init__()

        self.log = LogBase.log(self.__class__.__name__)
        self.__settings = Settings()
        self.__name = name
        self.__loader = loader
        self.__storage = storage
        self.log.debug("Initialized block {}".format(self.__name))

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


PluginLoader.load_plugins(sources=BlockSources)
