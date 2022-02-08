import asyncio
import logging
import requests


logger = logging.getLogger(__name__)


async def try_connect(url):
    result = requests.put(url)
    print(result.status_code)
    return result.status_code == 200


async def do_connect(url: str, max_trials=4, sleep_interval=3):
    trials = 1
    connected = False
    while trials < max_trials and connected == False:
        logger.info(f'Attempting to connect to {url}. Attempt {trials}')
        # try:
        res = await try_connect(url)
        if res:
            connected = True
            break
        # except:

        #     pass

        trials = trials + 1
        logger.info(f'Unable to connect to {url} - waiting 3s')
        await asyncio.sleep(sleep_interval)

    return connected
