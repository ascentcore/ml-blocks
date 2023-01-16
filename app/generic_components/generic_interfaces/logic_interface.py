from app.generic_components.generic_types.error import ErrorNotImplemented


class LogicInterface(object):

    def __init__(self):
        pass

    def setup(self, *args):
        """
        Interface setup functionality
        """
        raise ErrorNotImplemented()

    def start(self):
        """
        Interface start logic functionality
        """
        raise ErrorNotImplemented()

    def stop(self):
        """
        Interface stop logic functionality
        """
        raise ErrorNotImplemented()
