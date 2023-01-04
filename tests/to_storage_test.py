import os
import csv
import unittest
import random

from app.flow import Flow
from app.base_block import BaseBlock
from app.loaders.file_loader import FileLoader
from app.storage.in_memory_storage import InMemoryStorage
from app.settings import Settings

from tests.utils import prepare_local_files


class LoaderBlock(BaseBlock):

    name = os.getenv("BLOCK_NAME", "Loader Test Block ")

    root_loaders_classes = [FileLoader]

    storage_class = InMemoryStorage

    def __init__(self, settings):
        super().__init__(settings)

class ItemizerBlock(LoaderBlock):

    def itemize(self, file, loader):
        with open(file, newline='\n') as data:
            rows = csv.reader(data, delimiter=',')
            for index, row in enumerate(rows):
                if index > 0 and len(row) > 0:
                    yield [row[0], float(row[1]), float(row[2]), float(row[3])]


class TestFileStorage(unittest.TestCase):

    def test_loader_content_storage(self):
        prepare_local_files(True, 'first')
        prepare_local_files(False, 'second')
        settings = Settings()
        settings.MOUNT_FOLDER = 'stores'
        block = ItemizerBlock(settings)
        flow = Flow(block)

        flow.to_storage()
        self.assertEqual(block.storage.count(), 600)
        prepare_local_files(False, 'third')
        self.assertEqual(block.storage.count(), 600)
        block.root_loaders[0].refresh()
        flow.to_storage()
        self.assertEqual(block.storage.count(), 900)
        self.assertEqual(len(block.storage.query(0, 2)), 2)


    def test_loader_storage(self):
        prepare_local_files(True, 'first')
        prepare_local_files(False, 'second')
        settings = Settings()
        settings.MOUNT_FOLDER = 'stores'
        block = LoaderBlock(settings)
        flow = Flow(block)
        block.root_loaders[0].refresh()
        flow.to_storage()
        self.assertEqual(block.storage.count(), 2)
        self.assertEqual(block.storage.query(0, 2), ['stores/file_loader_files/tmp_first.csv', 'stores/file_loader_files/tmp_second.csv'])
