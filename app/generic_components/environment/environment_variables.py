from enum import Enum
from typing import Any, Dict

from app.generic_components.environment.environment import Environment
from app.generic_components.generic_types.error import ErrorNotImplemented
from app.generic_components.log_mechanism.log_mechanism import LogBase


class VariableSource(Enum):
    code = 0
    environment = 1
    json_config = 2,
    custom = 3


class VariableProperties(object):
    __name: str = ""
    __default_value = None
    __source = False
    __custom_call = None

    def __init__(self, name, default_value=None, source: VariableSource = VariableSource.code, custom_load = None):
        self.__name = name
        self.__default_value = default_value
        self.__source = source
        self.__custom_call = custom_load

    @property
    def name(self):
        return self.__name

    @property
    def default_value(self):
        return self.__default_value

    @property
    def from_environment(self):
        return self.__source == VariableSource.environment

    @property
    def from_json(self):
        return self.__source == VariableSource.json_config

    @property
    def from_code(self):
        return self.__source == VariableSource.code

    @property
    def custom_call(self):
        return  self.__custom_call


class Variable:
    __value = None
    __property: VariableProperties = None

    def __init__(self, properties: VariableProperties):
        super().__init__()
        self.log = LogBase.log(self.__class__.__name__)
        self.__property = properties
        self.load()

    def load(self):
        var_property = self.__property
        if self.__property.from_code:
            self.__value = var_property.default_value
        elif self.__property.from_environment:
            self.__value = Environment.value(variable_name=var_property.name,
                                             default_value=var_property.default_value)
        elif self.__property.custom_call:
            self.__value = self.__property.custom_call()
        else:
            raise ErrorNotImplemented()

    @property
    def value(self):
        return self.__value

    @property
    def name(self):
        return self.__property.name
