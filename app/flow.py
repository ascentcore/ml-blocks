import logging
import asyncio
import pickle

from app.settings import initialize_folder

# from app.listeners import load_data_file

logger = logging.getLogger(__name__)

class Flow:

    schedules = {}

    def __init__(self, block):
        self.block = block
        initialize_folder('models')
        self.to_storage()
        logger.info(f'Flow initialized {self.block.name}')


    def initialize_model(self):
        try:
            logger.info('Loading model')
            model = self.block.load_model()
            if model != None:
                logger.info(f'Loaded model: {model}')
                self.model = model
            else:
                logger.info('load_model method not provided. Downgrading to pickle')
                try:
                    infile = open(f'{self.block.settings.MOUNT_FOLDER}/models/model.pkl', 'rb')
                    model = pickle.load(infile)
                    infile.close()
                except:
                    logger.info('No model found, starting with empty state')
                    pass
        except Exception as e:
            logger.info(f'No model found, training new model: {e}')

    def to_storage(self,from_scratch = False):
        loaders = self.block.root_loaders

        root_loader = loaders[0]
        
        if (from_scratch == True):
            self.block.storage.clear()

        # for now we are just working with the root entry
        for data in root_loader.entries():
            if (self.block.storage.is_completed(data)):
                logger.info(f'Entry already parsed, skipping...')
                continue

            logger.info(f'New entry found, parsing...')
            for item in self.block.itemize(data, root_loader):
                if (self.block.filter(item, root_loader)):
                    self.block.storage.store(item)                    
                else:
                    logger.info(f'Rejected: {item}')
            self.block.storage.set_completed(data)
        
        logger.info(f'Stored {self.block.storage.count()} items')

        # logger.info('Preparing to train model')
        # self.run_fn_in_background(self._train_model, 'Train Model')
        # logger.info('Ingestion complete')

    # def register(self, hostname):
    #     data = load_data_file('data')
    #     data[hostname]

    async def build_model(self):
        model = await self.block.train()
        if model != None:
            logger.info(f'Trained model: {model}')
            if (self.block.save_model(model)):
                logger.info('Model saved')
            else:
                logger.info('Method save_model not provided. Downgrading to pickle')
                outfile = open(f'{self.block.settings.MOUNT_FOLDER}/models/model.pkl', 'wb')
                pickle.dump(model, outfile)
                outfile.close()
        else:
            logger.info('No model trained')


    def query(self, page=0, count=100):
        return self.block.storage.query(page, count)


    def run_fn_in_background(self, fn: callable, name='Untitled Background'):
        logger.info(f'Running {name} in background')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            loop.create_task(fn())
        else:
            asyncio.run(fn())


    # def schedule_fn_call(self, callback: callable, interval: int, name='Untitled Schedule'):
    #     logger.info(
    #         f'Schedule [{name}] scheduled to run every {interval} seconds')
    #     try:
    #         loop = asyncio.get_running_loop()
    #     except RuntimeError:
    #         loop = None

    #     id = f'schedule-{random.randint(100, 999)}'

    #     if loop and loop.is_running():
    #         loop.create_task(self.perform_schedule_execution(
    #             id, callback, interval, name))
    #     else:
    #         asyncio.run(self.perform_schedule_execution(
    #             id, callback, interval, name))

    #     self.schedules[id] = {
    #         "state": True
    #     }

    # async def perform_schedule_execution(self, id: str, fn: callable,  interval: int, name: str):
    #     while True:
    #         if self.schedules[id]["state"] is True:
    #             try:
    #                 logger.info(f'Running scheduled call {name} with {id}')
    #                 fn()
    #             except Exception as e:
    #                 logger.error(f'Error while running schedule call {name}')
    #                 logger.exception(e)
    #                 pass

    #             if interval > 0:
    #                 await asyncio.sleep(interval)
    #             else:
    #                 break