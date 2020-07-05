import asyncio
from aiohttp import ClientSession

def async_get(urls):
    async def fetch(url, session):
        async with session.get(url) as response:
            return await response.read()

    async def run(urls):
        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            for url in urls:
                task = asyncio.ensure_future(fetch(url, session))
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