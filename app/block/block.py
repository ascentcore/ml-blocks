import logging
import os

logger = logging.getLogger(__name__)


class Block:
    name = os.getenv("BLOCK_NAME", "Pass Through ML Block")

    def on_initialize(self, runtime):
        logger.info(f'echo: on_initialize')

    def on_before_store(self, runtime):
        logger.info(f'echo: on_before_store')

    def on_after_store(self, runtime):
        logger.info(f'echo: on_after_store')
