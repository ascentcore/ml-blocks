from .archive import ArchiveLoader
from .pandas import PandasLoader
from .loader import Loader

def get_loader(type: str) -> Loader:
    
    if type == None:
        return PandasLoader
    elif type.lower() == 'archive':
        return ArchiveLoader
    else:
        return PandasLoader

    