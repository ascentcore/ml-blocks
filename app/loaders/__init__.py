from .file_loader import FileLoader
from .pandas_loader import PandasLoader


def get_loader(type: str, settings):

    if type is None:
        return FileLoader(settings=settings)
    elif type.lower() == 'file_loader':
        return FileLoader(settings=settings)
    elif type.lower() == 'pandas_loader':
        return PandasLoader(settings=settings)

    raise Exception(
        f'Unkown pre-build loader {type}. Did you meant to pass a class?')
