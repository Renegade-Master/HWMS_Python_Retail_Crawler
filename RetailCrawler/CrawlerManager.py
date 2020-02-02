from json import loads
from queue import Queue

from Crawler import Crawler
import HwmsTools as hwms


class CrawlerManager:
    """ Class: Crawler Manager
    This class handles the Web Crawlers that are created to search for
    the provided RequestString.
    """

    _crawlers = []
    _item_response_strings = Queue()

    _item_requested = ''

    def __init__(self, eventstring):
        self.raw_request_string = loads(eventstring)

    def load_crawlers(self):
        # Extract the first item in the Request Dictionary Object
        self._item_requested = (
            self.raw_request_string
            ['Records'][0]['dynamodb']["NewImage"]["item"]["S"]
        )

        for retailer in hwms.Retailer.__iter__():
            self._crawlers.append(Crawler(
                hwms.format_search_term(self._item_requested, retailer),
                hwms.define_xpath(retailer)
            ))

        # Start the Crawlers
        for crawler in self._crawlers:
            crawler.start()
            crawler.join()
