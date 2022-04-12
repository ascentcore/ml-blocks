from app.loaders.pandas_loader import PandasLoader
from .file_loader import FileLoader


def get_loader(type: str, settings):

    if type == None:
        return FileLoader(settings=settings)
    elif type.lower() == 'file_loader':
        return FileLoader(settings=settings)
    elif type.lower() == 'pandas_loader':
        return PandasLoader(settings=settings)
    else:
        raise Exception(
            f'Unkown pre-build loader {type}. Did you meant to pass a class?')
