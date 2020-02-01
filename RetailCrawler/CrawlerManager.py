from enum import Enum
from json import loads
from re import IGNORECASE, compile
from queue import Queue, Empty

from Crawler import Crawler


class CrawlerManager():
    """ Class: Crawler Manager
    This class handles the Web Crawlers that are created to search for
    the provided RequestString.
    """

    _crawlers = []
    _cleaned_request_strings = []
    _item_response_strings = Queue()

    _search_request_string = ''
    _item_requested = ''

    def __init__(self, eventstring):
        self.raw_request_string = loads(eventstring)

    def load_crawlers(self):
        # Extract the first item in the Request Dictionary Object
        self._item_requested = (
            self.raw_request_string
            ['Records'][0]['dynamodb']["NewImage"]["item"]["S"]
        )

        for retailer in Retailer:
            self._cleaned_request_strings.append(
                self._format_search_term(self._item_requested, retailer))

        for term in self._cleaned_request_strings:
            self._crawlers.append(Crawler(term, 'null'))

        for crawler in self._crawlers:
            crawler.start()
            crawler.join()

    def _format_search_term(self, item_, retailer_):
        repl = ''
        regex = compile(r'\s', IGNORECASE)

        # Format the term however the Retailer is expecting
        if (retailer_ == Retailer.UK_ARIA or
                retailer_ == Retailer.UK_SCAN or
                retailer_ == Retailer.DE_CASEKING):
            repl = '+'
        else:
            raise ValueError('CrawlerManager._format_search_term: '
                             'Unsupported or missing value provided for'
                             ' Retailer.')

        clean_string = regex.sub(repl, item_)

        # print('Cleaned String: ' + clean_string)

        # Format the search URL.
        # ToDo: Move the retailer specific Strings to an external file
        #  that is read in
        search_url = ''

        if retailer_ == Retailer.UK_ARIA:
            search_url = \
                'https://www.aria.co.uk/Products?search={0}&x=0&y=0' \
                .format(clean_string)
        elif retailer_ == Retailer.UK_SCAN:
            search_url = \
                'https://www.scan.co.uk/search?q={0}' \
                .format(clean_string)
        elif retailer_ == Retailer.DE_CASEKING:
            search_url = \
                'https://www.caseking.de/search?sSearch={0}' \
                .format(clean_string)

        print('Search URL: ' + search_url)
        return search_url


class Retailer(Enum):
    UK_ARIA = 1
    UK_SCAN = 2
    DE_CASEKING = 3
