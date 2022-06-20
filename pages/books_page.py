import logging
import re

from bs4 import BeautifulSoup

from locators.books_on_page_locators import BooksOnPageLocator
from locators.pages_amount_locator import PagesAmountLocator
from parsers.book import BookParser

logger = logging.getLogger('scraping.books_page')


class BooksPage:
    """
    Return list of parsed book objects.
    """

    def __init__(self, page):
        logger.debug('Parsing page content with BS html parser')
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all books on page using `{BooksOnPageLocator.BOOK}` locator')
        locator = BooksOnPageLocator.BOOK
        books_li = self.soup.select(locator)
        return [BookParser(b) for b in books_li]

    @property
    def pages_amount(self):
        logger.debug(f'Finding pages amount using `{PagesAmountLocator.PAGES_AMOUNT}` locator')
        locator = PagesAmountLocator.PAGES_AMOUNT
        pages_am = self.soup.select_one(locator).string
        logger.info(f'Found pages amount: `{pages_am}`.')
        regex = 'Page [1-9]+ of ([0-9]+)'
        match = re.search(regex, pages_am)
        res = int(match.group(1))
        logger.debug(f'Extracted pages amount as int: `{res}`')
        return res
