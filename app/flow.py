import logging
import time
from app.block.block import Block
from app.decorators.singleton import singleton
from app.settings import settings
from app.runtime import Runtime
from app.loaders import get_loader

logger = logging.getLogger(__name__)


@singleton
class Flow:

    loaders = []

    def __init__(self, touch):
        logger.info('Flow initialized...')
        self.block = Block()
        self._touch_file = touch

        self.runtime = self._prepare_runtime_object()

        self.call_method('on_initialize', self.runtime)
        logger.info(
            f'Block: "{self.block.name}" [Host: {settings.HOST}] runtime initialized.')

    def _pass_through_process_fn(self, loader, dataset):
        return dataset

    def _prepare_runtime_object(self):
        runtime = Runtime()
        runtime.report_progress = self.report_progress
        runtime.settings = settings

        if hasattr(self.block, 'loaders'):
            prev_loader_content = None
            loaders = []
            for loader in self.block.loaders:
                loader_implementation = None
                if isinstance(loader, str):
                    logger.info(f'Trying to initialize loader {loader}')
                    try:
                        loader_implementation = get_loader(loader, settings)
                        loader_implementation.process_fn = getattr(self.block, 'process_data') if hasattr(
                            self.block, 'process_data') else self._pass_through_process_fn
                    except Exception as e:
                        logger.error(
                            f'Unable to initialize loader {loader}. Root Cause: {e}')
                else:
                    loader_implementation = loader

                if loader_implementation != None:
                    prev_loader_content = loader_implementation.initialize(
                        settings, prev_loader_content)
                    loaders.append(loader_implementation)

                self.loader = loader_implementation
            self.loaders = loaders

        return runtime

    def load_data_files(self, files, append):
        if not append:
            for loader in self.loaders:
                loader.clean()

        for file in files:
            last_content = file
            for loader in self.loaders:
                last_content = loader.load_content(last_content)
                logger.info(last_content)

        self._touch_file('data')

    def call_method(self, method: str, *args, **kwargs):
        if hasattr(self.block, method):
            method_to_call = getattr(
                self.block, method)
            return method_to_call(*args, **kwargs)

    def report_progress(self, percent: int):
        logger.info(f'Reporting progress... {percent}%')
        return None

    def set_error_state(self, state):
        pass

    ''' 
    Global Changes Event Listeners
    Some aspects of the flow should be reinitialized when one application thread
    is making any change to data or the models
    '''

    def data_update(self):
        logger.info('Data updated triggering loaders')
        prev_loader = None
        for loader in self.loaders:
            loader.initialize(settings, prev_loader)
            prev_loader = loader

    def model_update(self):
        logger.info('Model updated')
