import asyncio
import logging
import requests

logger = logging.getLogger(__name__)


async def try_connect(url, method):
    method_to_call = getattr(requests, method)
    result = method_to_call(url)
    return result.status_code == 200


async def do_connect(url: str, method='put', max_trials=5, sleep_interval=5):
    trials = 1
    connected = False
    while trials < max_trials and connected == False:
        logger.info(f'Attempting to connect to {url}. Attempt {trials}')
        try:
            res = await try_connect(url, method)
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


def connect(url, method='put', max_trials=5, sleep_interval=5):
    logger.info('Trying to connect to dependency')
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        loop.create_task(do_connect(url, method, max_trials, sleep_interval))
    else:
        asyncio.run(do_connect(url, method, max_trials, sleep_interval))
