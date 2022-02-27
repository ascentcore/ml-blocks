import asyncio
import logging
import requests

logger = logging.getLogger(__name__)

async def try_connect(url):
    result = requests.put(url)
    return result.status_code == 200


async def do_connect(url: str, max_trials=5, sleep_interval=5):
    trials = 1
    connected = False
    while trials < max_trials and connected == False:
        logger.info(f'Attempting to connect to {url}. Attempt {trials}')
        try:
            res = await try_connect(url)
            if res:
                connected = True
                break
        except:
            logger.info(
                f'Unable to connect to host {url}. Trials left {max_trials-trials}')
            pass

        trials = trials + 1
        logger.info(f'Unable to connect to {url} - waiting {sleep_interval}s')
        await asyncio.sleep(sleep_interval)

    return connected


async def trial_execute(fn, max_trials = 5, sleep_interval = 5):
    trials = 1
    succeeded = False
    while trials < max_trials and succeeded == False:
        try:
            fn()
            succeeded = True
            break
        except:
            logger.info(
                f'{fn.__name__} execution failed. Trials left {max_trials-trials}')
            pass

        trials = trials + 1
        await asyncio.sleep(sleep_interval)

    return succeeded