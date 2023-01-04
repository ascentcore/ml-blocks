import logging
import os

from app.loaders.file_loader import FileLoader
from app.base_block import BaseBlock

logger = logging.getLogger(__name__)

class Block(BaseBlock):

    name = os.getenv("BLOCK_NAME", "Pass Through ML Block")

