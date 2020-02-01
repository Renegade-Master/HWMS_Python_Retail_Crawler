import enum
import json
import re

import Crawler


class CrawlerManager:
    """ Class: Crawler Manager
    This class handles the Web Crawlers that are created to search for
    the provided RequestString.
    """

    _crawlers = []
    _cleaned_request_strings = []

    _search_request_string = ''
    _item_requested = ''

    def __init__(self, eventstring):
        self.raw_request_string = json.loads(eventstring)

    def load_crawlers(self):
        # Extract the first item in the Request Dictionary Object
        self._item_requested = (
            self.raw_request_string
            ['Records'][0]['dynamodb']["NewImage"]["item"]["S"]
        )

        for retailer in Retailer:
            self._cleaned_request_strings.append(
                self._format_search_term(self._item_requested, retailer))

        return self._item_requested

    def _format_search_term(self, item_, retailer_):
        repl = ''

        regex = re.compile(r'\s', re.IGNORECASE)

        # Format it however the Retailer is expecting
        if (retailer_ == Retailer.UK_SCAN or
                retailer_ == Retailer.UK_ARIA):
            repl = '+'
        else:
            raise ValueError('CrawlerManager._format_search_term: '
                             'Unsupported or missing value provided for'
                             ' Retailer.')

        clean_string = regex.sub(repl, item_)

        print('Cleaned String: ' + clean_string)

        return clean_string


class Retailer(enum.Enum):
    UK_SCAN = 1
    UK_ARIA = 2
