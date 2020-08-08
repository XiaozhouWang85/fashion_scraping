import json
import asyncio
from aiohttp import ClientSession
from google.cloud import logging
from google.cloud.logging.resource import Resource

from src import params

class gcp_logger:
    def __init__(self):
        log_client = logging.Client(params.GOOGLE_CLOUD_PROJECT)
        log_name = "cloudfunctions.googleapis.com%2Fcloud-functions"
        self.res = Resource(type="cloud_function", 
                       labels={
                           "function_name": params.GOOGLE_CLOUD_PROJECT, 
                           "region": params.GOOGLE_CLOUD_REGION
                       },
                      )
        self.logger = log_client.logger(log_name.format(params.GOOGLE_CLOUD_PROJECT))
    
    def log_struct(self, log_dict,severity):
        self.logger.log_struct(log_dict, resource=self.res, severity=severity)
        return 'Wrote logs to {}.'.format(self.logger.name)

def get_gcp_logger():
    return gcp_logger()

def async_get_all(urls, payload=None):
    async def fetch(url, session, **kwargs):
        async with session.get(url,**kwargs) as response:
            return await response.read()

    async def run(urls,payload=payload):
        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            if payload is None:
                for url in urls:
                    task = asyncio.ensure_future(fetch(url, session))
                    tasks.append(task)
            else:
                for url, params in zip(urls,payload):
                    task = asyncio.ensure_future(fetch(url, session, params=params))
                    tasks.append(task)
            responses = await asyncio.gather(*tasks)
            # you now have all response bodies in this variable
            return responses

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    return loop.run_until_complete(future)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def async_get(urls, payloads=None):
    if payloads is None:
        response_contents = [
            item for url_chunk in chunks(urls,params.ASYNC_CONN_NUM) \
            for item in async_get_all(url_chunk)
        ]
    else:
        #Chunk feature not implemented on version containing payload
        response_contents = async_get_all(urls,payloads)

    return response_contents

def async_post(urls, payloads):
    async def fetch(url, session, payload):
        async with session.post(url,data = json.dumps(payload)) as response:
            return await response.read()

    async def run(urls,payloads=payloads):
        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession(headers={'Content-Type': 'application/json'}) as session:
            for url, params in zip(urls,payloads):
                task = asyncio.ensure_future(fetch(url, session, payload=params))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            # you now have all response bodies in this variable
            return responses

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    return loop.run_until_complete(future)