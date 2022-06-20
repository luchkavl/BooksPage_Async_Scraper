import logging

from app import books

logger = logging.getLogger('scraping.menu')

USER_CHOICE = """Enter one of the following

- 'b' to look at 5-star books
- 'c' to look at the cheapest books
- 'n' to just get the next available book on the page
- 'q' to exit

Enter your choice:  """


def print_best_books():
    logger.info('Finding best books by rating...')
    best_books = [book for book in books if book.rating == 5]
    for book in best_books:
        print(book)


def print_cheapest_books():
    logger.info('Finding cheapest books...')
    cheapest_books = sorted(books, key=lambda x: x.price)
    for book in cheapest_books:
        print(book)


books_generator = (x for x in books)


def print_next_book():
    logger.info('Finding next book in generator of all books...')
    try:
        print(next(books_generator))
    except StopIteration:
        logger.debug('Caught StopIteration error')
        print('There is no more book at the page!')


user_choices = {
    'b': print_best_books,
    'c': print_cheapest_books,
    'n': print_next_book
}


def menu():
    user_input = input(USER_CHOICE).lower()
    while user_input != 'q':
        if user_input in user_choices.keys():
            user_choices[user_input]()
        else:
            print('Wrong command. Try another!')
        user_input = input(USER_CHOICE)
        logger.debug('Terminating program.')


menu()

