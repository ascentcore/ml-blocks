class BaseLoader:

    def initialize(self):
        pass

    def refresh(self):
        pass

    def query(self, page=0, count=100, format='raw'):
        raise NotImplementedError()