import logging
import os



logger = logging.getLogger(__name__)


class Block:
    name = os.getenv("BLOCK_NAME", "File Loader")

    loaders = ['file_loader']
