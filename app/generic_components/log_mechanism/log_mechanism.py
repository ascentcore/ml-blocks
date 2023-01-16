import logging
from enum import Enum

from app.generic_components.file_wrapper.file_wrapper import WrapperFile
from app.generic_components.singleton_base.singleton_base import Singleton


class LogOutputType(Enum):
    """
    Types of output streams
    """
    deactivated = 0
    console = 1
    file = 2
    all_activated = 3


class LogOutput(object):
    """
    Log Output helper class
    """

    @staticmethod
    def is_active(value, value_compare):
        """
        Checks if the output is active or not
        """
        return value == LogOutputType.all_activated or value == value_compare


# TODO add to settings
class LogDefaults(object):
    """
    Default log default
    """
    application_name = "App"
    file_log = "console.log"
    level = logging.DEBUG
    format = '%(asctime)s|%(levelname)5s|%(name)25s|%(thread)5x|%(filename)20s|%(funcName)15s|%(lineno)3s|%(message)s'
    output = LogOutputType.all_activated
    clear_on_start = True


class LogProperties(metaclass=Singleton):

    def __init__(self, configuration=LogDefaults()):
        self.__logger = None
        self.__configuration = configuration
        self.create_logger()

    @property
    def configuration(self):
        return self.__configuration

    @configuration.setter
    def configuration(self, value):
        self.__configuration = value

    def configure_console(self, formatter):
        """
        Add console configure
        """
        if LogOutput.is_active(self.configuration.output, LogOutputType.console):
            handler_stream = logging.StreamHandler()
            handler_stream.setLevel(self.configuration.level)
            handler_stream.setFormatter(formatter)
            self.__logger.addHandler(handler_stream)

    def configure_file_stream(self, formatter):
        """
        Add file stream configure
        """
        if LogOutput.is_active(self.configuration.output, LogOutputType.file):
            if self.configuration.clear_on_start:
                WrapperFile.remove(path=self.configuration.file_log)
            handler_file = logging.FileHandler(self.configuration.file_log)
            handler_file.setLevel(self.configuration.level)
            handler_file.setFormatter(formatter)
            self.__logger.addHandler(handler_file)

    def create_logger(self):
        """
        Create the logging object with all configuration
        """
        self.__logger = logging.getLogger(self.configuration.application_name)
        self.__logger.setLevel(self.configuration.level)

        formatter = logging.Formatter(self.configuration.format)
        self.configure_console(formatter=formatter)
        self.configure_file_stream(formatter=formatter)

    @property
    def logger(self):
        """
        Get logger object
        """
        return self.__logger


class LogBase:

    @staticmethod
    def log(class_name):
        """
        Get logging object already configured
        """
        main_logger = LogProperties()
        return main_logger.logger.getChild(class_name)


LOG = LogBase().log("root")
