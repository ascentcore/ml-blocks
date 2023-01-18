from app.generic_components.generic_types.error import ErrorNotImplemented
from app.generic_components.log_mechanism.log_mechanism import LOG
import app.block.storage
import app.logic.block.storage.types
from app.generic_components.plugin_loader.plugin_loader import PluginLoader

# where to search for extensions
BlockSources = [app.logic.block.storage.types.__file__, app.block.storage.__file__]


class BlockStorage:
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

    def __init__(self, name=""):
        self.__stored_state = []
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def clear(self):
        self.__stored_state = []

    def is_completed(self, data):
        return hash(data) in self.__stored_state

    def set_completed(self, data):
        self.__stored_state.append(hash(data))

    def count(self):
        raise ErrorNotImplemented()

    def store(self, item):
        raise ErrorNotImplemented()

    def query(self, page=0, count=100):
        raise ErrorNotImplemented()


PluginLoader.load_plugins(sources=BlockSources)
