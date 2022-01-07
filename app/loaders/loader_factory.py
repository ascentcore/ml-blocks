from .csv_loader import CSVLoader
# from .zip_loader import ZIPLoader
from .loader import Loader

switches = {
    "csv": CSVLoader,
    # "zip": ZIPLoader
}

def get_loader(loader_type, config = None) -> Loader:
    return switches[loader_type](config)
        