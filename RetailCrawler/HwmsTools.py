from enum import Enum
from re import compile, IGNORECASE


def format_search_term(item_, retailer_):
    """ Function: format_search_term
    This function is used to convert a provided Item, and create a
    URL to a store page.
    """

    repl = ''
    regex = compile(r'\s', IGNORECASE)  # Look for spaces to replace

    # Format the term however the Retailer is expecting
    # if (retailer_ == Retailer.DE_AMAZON or
    #         retailer_ == Retailer.DE_CASEKING or
    #         retailer_ == Retailer.NO_KOMPLETT or
    #         retailer_ == Retailer.UK_AMAZON or
    #         retailer_ == Retailer.UK_ARIA or
    #         retailer_ == Retailer.UK_SCAN):
    #     repl = '+'
    # else:
    #     raise ValueError('CrawlerManager._format_search_term: '
    #                      'Unsupported or missing value provided for'
    #                      ' Retailer.')

    repl = '+'
    clean_string = regex.sub(repl, item_)

    # Format the search URL.
    # ToDo: Move the retailer specific Strings to an external file
    #  that is read in
    search_url = ''

    if retailer_ == Retailer.DE_AMAZON:
        search_url = \
            'https://www.amazon.de/s?k={0}' \
            .format(clean_string)
    elif retailer_ == Retailer.DE_CASEKING:
        search_url = \
            'https://www.caseking.de/search?sSearch={0}' \
            .format(clean_string)
    elif retailer_ == Retailer.NO_KOMPLETT:
        search_url = \
            'https://www.komplett.ie/search-results/?tn_q={0}' \
            .format(clean_string)
    elif retailer_ == Retailer.UK_AMAZON:
        search_url = \
            'https://www.amazon.co.uk/s?k={0}' \
            .format(clean_string)
    elif retailer_ == Retailer.UK_ARIA:
        search_url = \
            'https://www.aria.co.uk/Products?search={0}' \
            .format(clean_string)
    elif retailer_ == Retailer.UK_SCAN:
        search_url = \
            'https://www.scan.co.uk/search?q={0}' \
            .format(clean_string)

    # print('Search URL: ' + search_url)
    return search_url


def define_xpath(retailer_):
    """ Function: define_xpath
    This function is used to create the XPath to the price data of
    different retailers.
    """

    # ToDo: Move the retailer specific Strings to an external file
    #  that is read in

    x_path = ''

    if retailer_ == Retailer.DE_AMAZON:
        x_path = \
            '/html/body/div[1]/div[1]/div[1]/div[2]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[2]/div/div[' \
            '1]/div/div/div[1]/h2/a/span '
    elif retailer_ == Retailer.DE_CASEKING:
        x_path = \
            '/html/body/div[6]/div/div/div/div/div[3]/div[4]/div[2]/div[1]/div/a[2]/span[2]'
    elif retailer_ == Retailer.NO_KOMPLETT:
        x_path = \
            '/html/body/div[1]/div/div[3]/div/div/div/div/div/div/div[4]/div[3]/div[1]/div[2]/h3/a/span'
    elif retailer_ == Retailer.UK_AMAZON:
        x_path = \
            '/html/body/div[1]/div[2]/div[1]/div[2]/div/span[4]/div[1]/div[3]/div/span/div/div/div[2]/div[2]/div/div[' \
            '1]/div/div/div[1]/h2/a/span '
    elif retailer_ == Retailer.UK_ARIA:
        x_path = \
            '/html/body/div[4]/div[1]/div[2]/div[2]/div/div/table/tbody/tr[2]/td[2]/strong/a'
    elif retailer_ == Retailer.UK_SCAN:
        x_path = \
            '/html/body/div[2]/div[3]/div/div/div/div/div[2]/ul[1]/li[1]/div[1]/span[2]/span[2]/a'

    # print('XPath: ' + x_path)
    return x_path


class Retailer(Enum):
    """ Enum: Retailer
    Enum to branch execution path based on different Retailers.
    """
    DE_AMAZON = 0
    DE_CASEKING = 1
    NO_KOMPLETT = 2
    UK_AMAZON = 3
    UK_ARIA = 4
    UK_SCAN = 5
