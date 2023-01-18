from enum import Enum
import app.logic.block.loader.types
import app.block.loader
from app.generic_components.generic_types.error import ErrorNotImplemented
from app.generic_components.log_mechanism.log_mechanism import LOG
from app.generic_components.plugin_loader.plugin_loader import PluginLoader


class BlockFormats(str, Enum):
    raw = "raw"
    application_json = "application/json"
    application_json_base64 = "application/json+base64"
    application_file = "application/file"


# where to search for extensions
BlockSources = [app.logic.block.loader.types.__file__, app.block.loader.__file__]


class BlockLoader:

    """Basic resource class. Concrete resources will inherit from this one
        """
    plugins = []

    # For every class that inherits from the current,
    # the class name will be added to plugins
    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        LOG.info(f">in {cls}")
        if type(cls) not in cls.plugins:
            cls.plugins.append(cls)

    def __init__(self, name="BlockLoaderFile"):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def formats(self):
        return ['raw', 'application/json', 'application/json+base64', 'application/file']

    def initialize(self):
        raise ErrorNotImplemented()

    def refresh(self):
        raise ErrorNotImplemented()

    def query(self, page=0, count=100, format='raw'):
        raise ErrorNotImplemented()

    def entries(self, format='application/file'):
        raise ErrorNotImplemented()


PluginLoader.load_plugins(sources=BlockSources)