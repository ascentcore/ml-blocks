import os
from typing.io import TextIO
from app.generic_components.generic_types.error import ErrorInvalidArgument, ErrorNotPresent


class WrapperFile:
    """
    File Handler class, used as a utility class for all file related tasks
    """

    @staticmethod
    def write_line(file_descriptor: TextIO, line: str):
        try:
            if "\n" not in line:
                line = line + "\n"
            file_descriptor.write(line)
        except:
            raise ErrorInvalidArgument(line)

    @staticmethod
    def write_multiline(file_descriptor: TextIO, lines: str):
        try:
            for line in lines:
                if "\n" not in line:
                    line = line + "\n"
                file_descriptor.write(line)
        except:
            raise ErrorInvalidArgument("")

    @staticmethod
    def open_file(path: str, flags: str, new_line ='\n'):
        """
        Get the file descriptor for a file
        :param path:
        :param flags:
        :param new_line:
        :return:
        """
        try:
            return open(path, flags, encoding='utf-8', errors='replace', newline=new_line)
        except:
            raise ErrorInvalidArgument(path)

    @staticmethod
    def get_filename(path:str):
        WrapperFile.is_present(path=path)
        return os.path.basename(path)


    @staticmethod
    def read_content(path: str, flags: str = "r"):
        """
        Get the file descriptor for a file
        :param path:
        :param flags:
        :return:
        """
        try:
            file_obj = open(path, flags, encoding='utf-8', errors='replace')
            return file_obj.read()
        except:
            raise ErrorInvalidArgument(path)

    @staticmethod
    def close_file(descriptor: TextIO):
        """
        Close file descriptor
        :return:
        """
        try:
            descriptor.close()
        except:
            raise ErrorInvalidArgument("")

    @staticmethod
    def write_to_file(path: str, lines: str):
        try:
            file_descriptor = WrapperFile.open_file(path=path, flags="wt")
            WrapperFile.write_multiline(file_descriptor=file_descriptor, lines=lines)
            WrapperFile.close_file(file_descriptor)
        except:
            raise ErrorInvalidArgument(path)

    @staticmethod
    def remove(path: str):
        """
        Removes a given file by path
        :param path: file path
        :return:
        """
        if not os.path.isfile(path):
            raise ErrorNotPresent(path)
        else:
            os.remove(path)

    @staticmethod
    def create_file(path: str, remove_on_exist: bool = False):
        """
        Create file by path
        :param path: file path
        :param remove_on_exist: flag that tell if we need to remove the present file
        :return: None, throws ErrorFileNotPresent if file is not present
        """
        if os.path.isfile(path) and remove_on_exist:
            WrapperFile.remove(path=path)
        open(path, 'a').close()

    @staticmethod
    def is_present(path: str):
        """
        Checks if file is present
        :param path: file path
        :return: None, throws ErrorFileNotPresent if file is not present
        """
        if not os.path.isfile(path):
            raise ErrorNotPresent(path)

    @staticmethod
    def get_absolute_path(root_folder_path: str, file_name: str):
        """
        Get the absolute file path
        :param root_folder_path: root folder of the file
        :param file_name: filename
        :return: absolute file path
        """
        return root_folder_path + os.sep + file_name

    @staticmethod
    def get_line_content(path: str, new_line ='\n'):
        """
        Returns the file content, throws exception if file is not present
        :param path: file path given
        :param new_line: flag that tells end of line
        :return: file content as an array
        """
        WrapperFile.is_present(path=path)
        with open(file=path, newline=new_line) as fp:
            lines = fp.readlines()
        return lines

    @staticmethod
    def is_extension_ok(path: str, extensions):
        for extension in extensions:
            if path.endswith(extension):
                return True
        return False

    @staticmethod
    def get_all_files_from_folder(path: str, extensions=None):
        files = []
        for current_path, current_subdir, current_files in os.walk(path):
            for name in current_files:
                if extensions is None:
                    files.append(os.path.join(current_path, name))
                else:
                    if WrapperFile.is_extension_ok(os.path.join(current_path, name), extensions):
                        files.append(os.path.join(current_path, name))
        return files
