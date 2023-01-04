class BaseStorage:

    def __init__(self):
        self.stored_state = []

    def clear(self):
        self.stored_state = []

    def is_completed(self, data):
        return hash(data) in self.stored_state

    def set_completed(self, data):
        self.stored_state.append(hash(data))