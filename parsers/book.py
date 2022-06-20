import re
import logging

from locators.book_locators import BookLocators

logger = logging.getLogger('scraping.book_parser')


class BookParser:
    """
    Accepts li with book items, can return each item data.
    """

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        logger.debug(f'Created book parser from `{parent}`')
        self.parent = parent

    def __repr__(self):
        return f'<Book {self.name}, £{self.price} ({self.rating} stars)>'

    @property
    def name(self):
        logger.debug('Finding book name...')
        locator = BookLocators.NAME
        name = self.parent.select_one(locator).attrs['title']
        logger.debug(f'Found book name: `{name}`')
        return name

    @property
    def price(self):
        logger.debug('Finding book price...')
        locator = BookLocators.PRICE
        price_str = self.parent.select_one(locator).string

        regex = '£([0-9]+\.[0-9]+)'
        match = re.search(regex, price_str)
        price = float(match.group(1))
        logger.debug(f'Found book price as float: `{price}`')
        return price

    @property
    def rating(self):
        logger.debug('Finding book rating...')
        locator = BookLocators.RATING
        rating_cls = self.parent.select_one(locator).attrs['class']
        rating_list = [rating for rating in rating_cls if rating != 'star-rating']
        rating = BookParser.RATINGS.get(rating_list[0])
        logger.debug(f'Found book rating: `{rating}`')
        return rating

    @property
    def link(self):
        logger.debug('Finding book link...')
        locator = BookLocators.LINK
        link = self.parent.select_one(locator).attrs['href']
        logger.debug(f'Found book link: `{link}`')
        return link
