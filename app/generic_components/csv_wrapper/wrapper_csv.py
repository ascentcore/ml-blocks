import csv

from app.generic_components.file_wrapper.file_wrapper import WrapperFile
from app.generic_components.generic_types.error import ErrorBase
from app.generic_components.log_mechanism.log_mechanism import LogBase, LOG


class WrapperCSV:

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(self.__class__.__name__)

    @staticmethod
    def is_not_empty(row):
        return len(row) > 0

    @staticmethod
    def discard_empty_rows(rows):
        _rows = []
        for index, row in enumerate(rows):
            if WrapperCSV.is_not_empty(row=row):
                _rows.append(row)
        return _rows

    @staticmethod
    def get_all_rows(path: str, delimiter=',', new_line='\n'):
        file_handler = WrapperFile.open_file(path=path, new_line=new_line)
        rows = csv.reader(csvfile=file_handler, delimiter=delimiter)
        WrapperFile.close_file(descriptor=file_handler)
        rows = WrapperCSV.discard_empty_rows(rows=rows)
        return rows

    @staticmethod
    def yield_rows(path: str, delimiter=',', new_line='\n', flags="rt", headers_also: bool = False):
        LOG.debug(f'Reading content from {path}')
        try:
            WrapperFile.is_present(path=path)
            with open(file=path, mode=flags, newline=new_line) as file_descriptor:
                csv_rows = csv.reader(file_descriptor, delimiter=delimiter)
                if headers_also:
                    yield next(csv_rows)
                else:
                    header = next(csv_rows)
                for row in csv_rows:
                    if WrapperCSV.is_not_empty(row=row):
                        yield row
        except ErrorBase:
            LOG.warn("Something went wrong")
