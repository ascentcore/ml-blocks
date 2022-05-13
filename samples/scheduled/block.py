import logging
import os
import time
import random
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class Block:
    name = os.getenv("BLOCK_NAME", "Scheduled Data")

    loaders = ['file_loader', 'pandas_loader']

    def on_initialize(self, runtime):
        logger.info('Initializing scheduled events...')
        logger.info(runtime.loader.dataset.dtypes)
        runtime.schedule_fn_call(self.fetch_data(runtime), 10)

    def fetch_data(self, runtime):

        cached_dataset = []

        def inner_fn():
            logger.info('Fetching data')

            for i in range(0, 50):
                cached_dataset.append([
                    time.ctime(time.time()),
                    random.random(),
                    random.random(),
                    random.choice([0, 1, 2, 3])])

            if len(cached_dataset) > 100:
                val = 'time,x,y,c\n'
                for row in cached_dataset:
                    val = val + (','.join([str(item) for item in row])) + '\n'

                content = {'filename': 'generated.csv', "content": val}
                runtime.load_data_content(content, False)
                cached_dataset.clear()

        return inner_fn

    def generate_statics(self, runtime):
        print('generating statics')
        data = runtime.loader.dataset
        data.plot.scatter(x='x', y='y', c='c',  colormap='viridis')
        plt.savefig(runtime.produce_statics_path('scatterplot.png'))
