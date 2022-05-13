import logging
import time

from app.block.block import Block
from app.decorators.singleton import singleton
from app.loaders import get_loader
from app.settings import settings
from app.runtime import Runtime

logger = logging.getLogger(__name__)

stages = ['load_data', 'generate_statics', 'train', 'pending']


@singleton
class Flow:

    loaders = []

    stage = 'pending'

    def __init__(self, touch):
        logger.info('Flow initialized...')
        self.block = Block()
        self._touch_file = touch

        self.runtime = self._prepare_runtime_object()

        self.call_method('on_initialize', self.runtime)
        logger.info(
            f'Block: "{self.block.name}" [Host: {settings.HOST}] runtime initialized.')

    def trigger(self, stage):
        logger.info(f'Moving block to stage {stage} and triggering execution')
        self.stage = stage
        self.next(increment=False)

    def next(self, increment=True):
        current_stage_idx = stages.index(self.stage)

        if increment:
            self.stage = stages[current_stage_idx+1]
        
        if self.stage is not 'pending':
            try:
                for local_stage in [f'on_before_{self.stage}', self.stage, f'on_after_{self.stage}']:
                    self.write_stage(local_stage)
                    self.call_method(local_stage, self.runtime)
                self.next()
            except Exception as e:
                # logger.error(e)
                logger.exception(e)
                self.report_error(local_stage)
      

    def write_stage(self, stage):
        with open(f'{settings.MOUNT_FOLDER}/internal/stage', 'w') as fp:
            fp.write(stage)
            fp.close()

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

                if loader_implementation is not None:
                    prev_loader_content = loader_implementation.initialize(
                        settings, prev_loader_content)
                    loaders.append(loader_implementation)

                self.loader = loader_implementation
            self.loaders = loaders
            runtime.loader = loader_implementation

        return runtime

    def load_data_files(self, files, append):
        if not append:
            for loader in self.loaders:
                loader.clean()

        self.call_method('on_before_load_data', self.runtime)

        try:
            for file in files:
                last_content = file
                for loader in self.loaders:
                    last_content = loader.load_content(last_content)
        except:
            self.report_error('load_data')

        self.call_method('on_after_load_data', self.runtime)
        self._touch_file('data')
        self.stage = 'generate_statics'
        self.next()

    def call_method(self, method: str, *args, **kwargs):
        logger.info(f'Trying to call {method}')
        if hasattr(self.block, method):
            method_to_call = getattr(
                self.block, method)
            return method_to_call(*args, **kwargs)

        return True

    def report_error(self, method):
        self.stage = f'{method}_error'
        self.write_stage(f'{method}_error')
        self.call_method('on_error', method, self.runtime)

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
        prev_loader_content = None
        for loader in self.loaders:
            prev_loader_content = loader.initialize(settings, prev_loader_content)

    def model_update(self):
        logger.info('Model updated')
