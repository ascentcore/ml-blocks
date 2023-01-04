import logging
import os

logger = logging.getLogger(__name__)


class Block:
    name = os.getenv("BLOCK_NAME", "Pass Through ML Block")

    loaders = ['file_loader']
