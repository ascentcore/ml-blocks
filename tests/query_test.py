import os
import csv
import unittest
from unittest import IsolatedAsyncioTestCase
import random

from app.flow import Flow
from app.base_block import BaseBlock
from app.loaders.file_loader import FileLoader
from app.storage.in_memory_storage import InMemoryStorage
from app.settings import Settings

from tests.utils import prepare_local_files, prepare_folder


class LoaderBlock(BaseBlock):

    name = os.getenv("BLOCK_NAME", "Loader Test Block ")

    root_loaders_classes = [FileLoader]

    storage_class = InMemoryStorage

    def __init__(self, settings):
        super().__init__(settings)

    async def train(self):
        print('>>>>> training')
        return {"w": 1, "b": 1}


class ItemizerBlock(LoaderBlock):

    def itemize(self, file, loader):
        with open(file, newline='\n') as data:
            rows = csv.reader(data, delimiter=',')
            for index, row in enumerate(rows):
                if index > 0 and len(row) > 0:
                    yield [row[0], float(row[1]), float(row[2]), float(row[3])]


class TestQueries(IsolatedAsyncioTestCase):

    async def test_simple_data_query(self):
        prepare_local_files(True, 'first')
        prepare_local_files(False, 'second')
        prepare_folder('stores/tests/models')

        settings = Settings()
        settings.MOUNT_FOLDER = 'stores/tests'
        block = ItemizerBlock(settings)
        flow = Flow(block)
        flow.to_storage()
        await flow.build_model()

        flow.initialize_model()
        print(flow.model)