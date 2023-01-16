
class Singleton(type):
    """
    Singleton class base
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Call class
        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
