import json
from app.generic_components.file_wrapper.file_wrapper import WrapperFile


class JsonObject(object):

    @staticmethod
    def read_json_content(path: str):
        WrapperFile.is_present(path=path)
        with open(path) as data_file:
            result = json.load(data_file)
        return result

    @staticmethod
    def write_json_file(path: str, content, remove_on_exist=False):
        WrapperFile.create_file(path=path, remove_on_exist=remove_on_exist)
        with open(path, 'w') as outfile:
            json.dump(content, outfile)
