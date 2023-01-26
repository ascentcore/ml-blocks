import os
import shutil

from app.generic_components.generic_types.error import ErrorNotPresent

try:
    from app.generic_components.log_mechanism.log_mechanism import LOG
except ImportError:
    pass


class FolderWrapper:
    """
    Folder Handler class, used as a utility class for all folder related tasks
    """

    @staticmethod
    def create_folder(path: str, delete_if_present: bool = False):
        """
        Create a folder if not present, or recreated it if flag is True
        """
        try:
            LOG.debug(f'creating {path}')
        except NameError:
            pass
        try:
            FolderWrapper.is_present(path=path)
            if delete_if_present:
                shutil.rmtree(path, ignore_errors=True)
                os.mkdir(path=path)  # TODO do not like the duplication
        except ErrorNotPresent:
            os.mkdir(path=path)
            try:
                LOG.debug(f'created {path} successfully')
            except NameError:
                pass

    @staticmethod
    def is_present(path: str):
        """
        Checks if folder  is present
        :param path: file path
        :return: None, throws ErrorNotPresent if is not present
        """
        if not os.path.exists(path):
            raise ErrorNotPresent(path)

    @staticmethod
    def get_absolute_path(path: str):
        """
        Transform in absolute path
        Args:
            path:
        Returns:
        """
        return os.path.abspath(path=path)

    @staticmethod
    def get_cwd():
        """
        Get current working dir
        Returns:
        """
        return os.path.abspath(os.getcwd())
