import os

from app.generic_components.generic_types.error import ErrorNotPresent


class Environment:

    def __init__(self):
        pass

    @staticmethod
    def value(variable_name: str, default_value=None, raise_warning=False):
        """
        Get the value of the environment
        :param variable_name: variable name
        :param default_value: default value
        :param raise_warning: raise error
        """
        try:
            if not raise_warning and default_value is not None:
                return os.getenv(key=variable_name, default=default_value)
            else:
                return os.getenv(key=variable_name)
        except KeyError:
            raise ErrorNotPresent("Key not present {}".format(variable_name))
