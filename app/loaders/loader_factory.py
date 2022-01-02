from .pandas_loader import PandasLoader
from .raw_loader import RawLoader
from .loader import Loader

switches = {
    "pandas": PandasLoader,
    "raw": RawLoader
}

def get_loader(loader_config, config) -> Loader:
    if isinstance(loader_config, str):
        return switches[loader_config](config)
    
    return loader_config
        