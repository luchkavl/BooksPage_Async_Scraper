import logging
import time
import asyncio
import aiohttp
import async_timeout
import requests

from pages.books_page import BooksPage

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO,
    filename='logs.txt'
)

logger = logging.getLogger('scraping')

logger.info('Loading books list...')

page_content = requests.get('https://books.toscrape.com/catalogue/page-1.html').content
page = BooksPage(page_content)

loop = asyncio.get_event_loop()

books = page.books


async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:  # asks server for response
            print(f'Page took {time.time() - page_start}')
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks

urls = [f'https://books.toscrape.com/catalogue/page-{page_num}.html' for page_num in range(2, page.pages_amount)]
start = time.time()

pages = loop.run_until_complete(get_multiple_pages(loop, *urls))

for page_content in pages:
    logger.debug('Creating AllBooksPage from page content.')
    page = BooksPage(page_content)
    print(time.time() - start)

    books.extend(page.books)
