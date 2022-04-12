import logging
import os

logger = logging.getLogger(__name__)

class Block:
    name = os.getenv("BLOCK_NAME", "Echo Block")

    def on_initialize(self, runtime):
        logger.info(f'echo: on_initialize')

    def on_before_data_ingest(self, runtime):
        logger.info(f'echo: on_before_data_ingest')

    def on_after_data_ingest(self, runtime):
        logger.info(f'echo: on_after_data_ingest')


    
