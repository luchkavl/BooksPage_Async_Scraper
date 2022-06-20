import aiohttp
import asyncio
import time

# You creating only one session for all, instead of creating a new session every time
import async_timeout


async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:  # asks server for response
            print(f'Page took {time.time() - page_start}')
            return response.status


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks

loop = asyncio.get_event_loop()

urls = ['http://google.com' for i in range(50)]
start = time.time()
loop.run_until_complete(get_multiple_pages(loop, *urls))  # it's creating and returns a coroutine object, not status
print(time.time() - start)
