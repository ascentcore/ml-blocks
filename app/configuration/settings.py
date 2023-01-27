import socket
from enum import IntEnum
from typing import List

from app.generic_components.environment.environment_variables import Variable, VariableProperties, VariableSource
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.singleton_base.singleton_base import Singleton


class VariableMap(IntEnum):
    PROJECT_NAME = 0
    RUN_ENV = 1
    VERSION = 2
    STORAGE_FOLDER = 3
    API = 4
    MOUNT_FOLDER = 5
    MESSAGE_BROKER = 6
    DATA_DEPENDENCY = 7
    LOGIC_DEPENDENCIES = 8
    REGISTRY = 9
    HOSTNAME = 10
    BLOCK_NAME = 11
    HOST = 12
    SQLITE_STORAGE = 13
    BLOCK_LOADER = 14
    BLOCK_STORAGE = 15


class Settings(metaclass=Singleton):
    # TODO maybe a faster way on the future
    __variables_properties = \
        [
            VariableProperties(name=VariableMap.PROJECT_NAME.name, default_value="ML-Blocks API"),
            VariableProperties(name=VariableMap.RUN_ENV.name, default_value="development",
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.VERSION.name, default_value="1.0.0"),
            VariableProperties(name=VariableMap.STORAGE_FOLDER.name, default_value="file_loader_files"),
            VariableProperties(name=VariableMap.API.name, default_value="/api/v1"),
            VariableProperties(name=VariableMap.MOUNT_FOLDER.name, default_value="/app/data",
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.MESSAGE_BROKER.name, default_value=None,
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.DATA_DEPENDENCY.name, default_value=None,
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.LOGIC_DEPENDENCIES.name, default_value=None,
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.REGISTRY.name, default_value=None,
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.HOSTNAME.name, default_value="localhost",
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.BLOCK_NAME.name, default_value="BlockSimple",
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.HOST.name,
                               default_value=str(socket.gethostbyname(socket.gethostname()))),
            VariableProperties(name=VariableMap.SQLITE_STORAGE.name,
                               default_value="file::memory:?cache=shared"),
                               #default_value="database.db"),
            VariableProperties(name=VariableMap.BLOCK_LOADER.name, default_value="BlockLoaderFile",
                               # TODO all str to have single entry point
                               source=VariableSource.environment),
            VariableProperties(name=VariableMap.BLOCK_STORAGE.name, default_value="BlockStorageMemory", # TODO all str to have single entry point
                               source=VariableSource.environment)
        ]

    def __init__(self):
        self.log = LogBase.log(self.__class__.__name__)
        self.__variables: List[Variable] = []
        self.load_variables()

    def load_variables(self):
        for properties in self.__variables_properties:
            variable = Variable(properties=properties)
            self.__variables.append(variable)

    @property
    def registry(self):
        return self.__variables[VariableMap.REGISTRY].value

    @property
    def block_name(self):
        return self.__variables[VariableMap.BLOCK_NAME].value
    def print(self):
        self.log.debug("Loaded values:")
        for variable in self.__variables:
            self.log.debug('\t {} = {}'.format(variable.name, variable.value))

    @property
    def mount_folder(self):
        return self.__variables[VariableMap.MOUNT_FOLDER].value

    @property
    def storage_folder(self):
        return self.__variables[VariableMap.STORAGE_FOLDER].value

    @property
    def api(self):
        return self.__variables[VariableMap.API].value

    @property
    def version(self):
        return self.__variables[VariableMap.VERSION].value

    @property
    def environment(self):
        return self.__variables[VariableMap.RUN_ENV].value

    @property
    def sqlite_database(self):
        return self.__variables[VariableMap.SQLITE_STORAGE].value

    @property
    def data_dependency(self):
        return self.__variables[VariableMap.DATA_DEPENDENCY].value

    def active_block(self):
        return self.__variables[VariableMap.BLOCK_NAME].value

    @property
    def active_block_loader(self):
        return self.__variables[VariableMap.BLOCK_LOADER].value

    @property
    def hostname(self):
        return self.__variables[VariableMap.HOSTNAME].value

    @property
    def active_block_storage(self):
        return self.__variables[VariableMap.BLOCK_STORAGE].value

    def get_variable(self, variable):
        return self.__variables[variable].value
