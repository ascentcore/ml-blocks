import asyncio
import requests
import urllib3.exceptions

from app.generic_components.log_mechanism.log_mechanism import LOG
import socket

async def try_connect(url, method):
    try:
       
        method_to_call = getattr(requests, method)
        result =  method_to_call(url)
        LOG.debug(f'Getting here {result} {url} {method} ')
        http_status_code = result.status_code
        LOG.debug(f'Status code received {http_status_code}')
    except : 
        http_status_code = 404
        LOG.warn(f' exception raised')

    return http_status_code == 200


async def connect(url: str, method='put'):
    try:
        res = await try_connect(url, method)
        LOG.debug(f'Connect to host {url} result {res}')
        return res
    except requests.exceptions.HTTPError as err:
        LOG.error(err)        
    LOG.warn(f'Unable to connect to host {url}')
    return False


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