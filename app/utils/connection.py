import asyncio
import requests

from app.generic_components.log_mechanism.log_mechanism import LOG


async def try_connect(url, method):
    method_to_call = getattr(requests, method)
    result = method_to_call(url)
    LOG.debug(f'Received status for {url}: {result.status_code}')
    return result.status_code == 200


async def do_connect(url: str, method='put', max_trials=5, sleep_interval=5):
    trials = 1
    connected = False
    while trials < max_trials and connected == False:
        LOG.info(f'Attempting to connect to {url}. Attempt {trials}')
        try:
            res = await try_connect(url, method)
            if res:
                connected = True
                break
        except requests.exceptions.HTTPError as err:
            LOG.error(err)
            LOG.info(
                f'Unable to connect to host {url}. Trials left {max_trials-trials}')
            pass

        trials = trials + 1
        LOG.info(f'Unable to connect to {url} - waiting {sleep_interval}s')
        await asyncio.sleep(sleep_interval)

    return connected


'''
Not used so far
'''


async def trial_execute(fn, max_trials=5, sleep_interval=5):
    trials = 1
    succeeded = False
    while trials < max_trials and succeeded == False:
        try:
            fn()
            succeeded = True
            break
        except:
            LOG.info(
                f'{fn.__name__} execution failed. Trials left {max_trials-trials}')
            pass

        trials = trials + 1
        await asyncio.sleep(sleep_interval)

    return 