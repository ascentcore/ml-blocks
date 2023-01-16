import logging
import os

from old.cached_version.base_block import BaseBlock

logger = logging.getLogger(__name__)

class Block(BaseBlock):

    name = os.getenv("BLOCK_NAME", "Pass Through ML Block")

