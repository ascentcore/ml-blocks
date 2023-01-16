import os
import sqlite3
import sys

from app.generic_components.file_wrapper.file_wrapper import WrapperFile
from app.generic_components.generic_types.error import ErrorNotPresent, ErrorInvalidUsage
from app.generic_components.log_mechanism.log_mechanism import LogBase


class WrapperSqlite:
    __connection = None

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(self.__class__.__name__)

    def is_connected(self):
        return self.__connection is not None

    def connect_database(self, path, force_create: bool = True, check_same_thread: bool = False):
        if self.is_connected():
            raise ErrorInvalidUsage("Already connected. Please disconnect first")

        try:
            if os.sep in path:
                WrapperFile.is_present(path)
            self.__connection = sqlite3.connect(path, check_same_thread=check_same_thread)
        except ErrorNotPresent:
            if not force_create:
                raise ErrorNotPresent(f'Not present {path}')
            else:
                WrapperFile.create_file(path=path)
                # TODO remove duplicate code
                self.__connection = sqlite3.connect(path)

    @staticmethod
    def to_blob(data):
        return sqlite3.Binary(data)

    def close_connection(self):
        if not self.is_connected():
            raise ErrorInvalidUsage("Already disconnected. Please connect first")
        self.__connection.close()
        self.__connection = None

    def create_custom_function(self, params, func_name, func_point):
        if self.is_connected():
            raise ErrorInvalidUsage("Already connected. Please disconnect first")

        if params and func_name and func_point:
            self.__connection.create_function(func_name, params, func_point)

        self.log.debug(f'Finished params {params} func_name {func_name} func_point {func_point}')

    def send_command(self, command, parameters=None, query: bool = False, multiple: bool = True):
        results = ""
        if not self.is_connected():
            raise ErrorInvalidUsage("Not connected")

        if command is not None:
            statement = self.__connection.cursor()
            try:
                if parameters:
                    statement.execute(command, parameters)
                else:
                    statement.execute(command)
                if query:
                    if multiple:
                        results = statement.fetchall()
                    else:
                        results = statement.fetchone()
                else:
                    self.__connection.commit()
            except sqlite3.OperationalError:
                raise ErrorInvalidUsage(f'Something is nok {command}  {parameters}')
        return results
