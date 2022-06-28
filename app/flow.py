import logging
import pickle
import json

from app.block.block import Block
from app.decorators.singleton import singleton
from app.loaders import get_loader
from app.settings import settings
from app.runtime import Runtime

logger = logging.getLogger(__name__)

default_stages = ['load_data', 'train', 'generate_statics']

@singleton
class Flow:

    loaders = []

    stage = 'pending'

    def __init__(self, touch):
        logger.info('Flow initialized...')
        self.block = Block()
        self._touch_file = touch

        logger.info(f'Initializing block {self.block.name}')

        self.runtime = self._prepare_runtime_object()

        self.block.load_model(self.runtime)
        self.preferences_update()

        self.call_method('on_initialize', self.runtime)
        logger.info(
            f'Block: "{self.block.name}" [Host: {settings.HOST}] runtime initialized.')

    def trigger(self, stage):
        logger.info(f'Moving block to stage {stage} and triggering execution')
        self.stage = stage
        self.next()

    def set_stage_and_execute(self, stage: str, stages=default_stages, data=None):
        self.stages = stages
        self.stage = stage
        self.runtime.last_op_data = data
        self.next()

    def next(self):
        current_stage_idx = self.stages.index(self.stage)
        logger.info('Executing stage: ' + self.stage)

        try:
            for local_stage in [f'on_before_{self.stage}', self.stage, f'on_after_{self.stage}']:
                logger.debug(f'> Executing local stage: {local_stage}')
                self.write_stage(local_stage)
                if hasattr(self.block, local_stage):
                    last_op_data = self.call_method(local_stage, self.runtime)
                    self.runtime.last_op_data = last_op_data
                if local_stage == 'train':
                    self.block.save_model(runtime=self.runtime)
                    self._touch_file('model')

            if current_stage_idx < len(self.stages) - 1:
                self.stage = self.stages[current_stage_idx+1]

                # Move this to a background task
                self.next()
            else:
                self.stage = 'pending'
        except Exception as e:
            # logger.error(e)
            logger.exception(e)
            self.report_error(local_stage)

        # if increment and len(self.stages):
        #     self.stage = self.stages[current_stage_idx+1]

    def write_stage(self, stage):
        with open(f'{settings.MOUNT_FOLDER}/internal/stage', 'w') as fp:
            fp.write(stage)
            fp.close()

    def _pass_through_process_fn(self, loader, dataset):
        return dataset

    def _prepare_runtime_object(self):

        logger.info('Preparing runtime object')
        runtime = Runtime()
        runtime.report_progress = self.report_progress
        runtime.settings = settings
        runtime.last_op_data = None

        logger.info(hasattr(self.block, 'loaders'))

        if hasattr(self.block, 'loaders'):
            prev_loader_content = None
            loaders = []
            for loader in self.block.loaders:
                logger.info(f'Trying to initialize loader {loader}')
                loader_implementation = None
                if isinstance(loader, str):

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

        def load_data_content(file, append):
            self.load_data_files([file], append)

        runtime.load_data_content = load_data_content

        for fn in [self.save_model, self.load_model, self.predict]:
            func_name = fn.__name__
            setattr(self.block, func_name, getattr(self.block, func_name) if hasattr(
                self.block, func_name) else fn)

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
        except Exception as e:
            logger.exception(e)
            self.report_error('load_data')

        self.call_method('on_after_load_data', self.runtime)
        self._touch_file('data')
        self.stages = ['train', 'generate_statics']
        self.stage = 'train'
        self.next()

    def call_method(self, method: str, *args, **kwargs):
        logger.info(f'Trying to call {method}')
        if hasattr(self.block, method):
            method_to_call = getattr(
                self.block, method)
            return method_to_call(*args, **kwargs)
       

    def report_error(self, method):
        self.stage = f'{method}_error'
        self.write_stage(f'{method}_error')
        self.call_method('on_error', self.runtime, method)

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
            prev_loader_content = loader.initialize(
                settings, prev_loader_content)

    def model_update(self):
        logger.info('Model updated, reloading model')
        self.block.load_model(self.runtime)

    def preferences_update(self):
        logger.info('Preferences updated. Reloading ...')
        try:
            self.runtime.preferences = json.loads(
                f'{self.runtime.settings.MOUNT_FOLDER}/internal/preferences.json')
        except Exception as e:
            logger.info('Unable to reload preferences')
            logger.error(e)

    def save_model(self, runtime):
        logger.info('Attempting to save model ...')
        runtime.model = runtime.last_op_data
        if runtime.model is None:
            raise Exception('train method returned no model to save')

        pickle.dump(runtime.model, open(
            f'{runtime.settings.MOUNT_FOLDER}/models/model.pkl', 'wb'))

        logger.info("Model saved successfully")

    def load_model(self, runtime):
        logger.info('Attempting to load_model')
        try:
            infile = open(
                f'{runtime.settings.MOUNT_FOLDER}/models/model.pkl', 'rb')
            self.runtime.model = pickle.load(infile)
            infile.close()
            logger.info('Model loaded successfully')
        except Exception as e:
            logger.error(e)

    def predict(self, runtime):
        return self.runtime.model.predict(runtime.last_op_data)
