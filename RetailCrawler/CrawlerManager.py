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
    _cleaned_request_strings = []
    _cleaned_xpaths = []
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

        for retailer in hwms.Retailer:
            self._cleaned_request_strings.append(
                hwms.format_search_term(self._item_requested, retailer))

        for retailer in hwms.Retailer:
            self._cleaned_xpaths.append(
                hwms.define_xpath(retailer))

        for i in range(len(self._cleaned_request_strings)):
            self._crawlers.append(Crawler(
                self._cleaned_request_strings[i],
                self._cleaned_xpaths[i]
            ))

        for crawler in self._crawlers:
            crawler.start()
            crawler.join()
