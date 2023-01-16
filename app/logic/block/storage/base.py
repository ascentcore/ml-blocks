from app.generic_components.generic_types.error import ErrorNotImplemented


class BlockStorage:

    def __init__(self):
        self.__stored_state = []

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
