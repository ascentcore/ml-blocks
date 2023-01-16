from enum import Enum

from app.generic_components.generic_types.error import ErrorNotImplemented


class BlockFormats(str, Enum):
    raw = "raw"
    application_json = "application/json"
    application_json_base64 = "application/json+base64"
    application_file = "application/file"


class BlockLoader:

    def __init__(self):
        pass

    def formats(self):
        return ['raw', 'application/json', 'application/json+base64', 'application/file']

    def initialize(self):
        raise ErrorNotImplemented()

    def refresh(self):
        raise ErrorNotImplemented()

    def query(self, page=0, count=100, format='raw'):
        raise ErrorNotImplemented()
