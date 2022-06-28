import logging
import random
import os
import time

import asyncio

from typing import Callable
from app.settings import settings


logger = logging.getLogger(__name__)


class Runtime:

    report_progress: Callable
    settings: settings

    schedules = {}

    def produce_statics_path(self, filename: str, safe: bool = True) -> str:
        if safe:
            file_name, file_extension = os.path.splitext(filename)
            return f'{settings.MOUNT_FOLDER}/statics/{file_name}-{int(time.time())}{file_extension}'
        else:
            return f'{settings.MOUNT_FOLDER}/statics/{filename}'

    def schedule_fn_call(self, callback: callable, interval: int, name='Untitled Schedule'):
        logger.info(
            f'Schedule [{name}] scheduled to run every {interval} seconds')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        id = f'schedule-{random.randint(100, 999)}'

        if loop and loop.is_running():
            loop.create_task(self.perform_schedule_execution(
                id, callback, interval, name))
        else:
            asyncio.run(self.perform_schedule_execution(
                id, callback, interval, name))

        self.schedules[id] = {
            "state": True
        }

    async def perform_schedule_execution(self, id: str, fn: callable,  interval: int, name: str):
        while True:
            if self.schedules[id]["state"] is True:
                try:
                    logger.info(f'Running scheduled call {name} with {id}')
                    fn()
                except Exception as e:
                    logger.error(f'Error while running schedule call {name}')
                    logger.exception(e)
                    pass

                await asyncio.sleep(interval)

    def predict(self, data):
        logger.info('Attempting to predict')
        result = self.model.predict(data)
        return result
