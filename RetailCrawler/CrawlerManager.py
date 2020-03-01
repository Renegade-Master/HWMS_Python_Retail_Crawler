from json import loads
from queue import Queue
from threading import Condition

from Crawler import Crawler
import HwmsTools as hwms


class CrawlerManager:
    """ Class: Crawler Manager
    This class handles the Web Crawlers that are created to search for
    the provided RequestString.
    """

    _crawlers = []
    _item_response_strings = Queue()
    _queue_condition = Condition()

    _item_requested = ''

    def __init__(self, eventstring):
        self.raw_request_string = loads(eventstring)

        # Extract the first item in the Request Dictionary Object
        self._item_requested = (
            self.raw_request_string
            ['Records'][0]['dynamodb']["NewImage"]["item"]["S"]
        )

    def load_crawlers(self):
        for retailer in hwms.Retailer.__iter__():
            self._crawlers.append(Crawler(
                hwms.format_search_term(self._item_requested, retailer),
                hwms.define_xpath(retailer)
            ))

        # Start the Crawlers
        for crawler in self._crawlers:
            crawler.start()
            crawler.join()

        # Start the Crawlers
        for crawler in self._crawlers:
            self._item_response_strings.put(crawler.result_of_search)

        self._item_response_strings.task_done()

        # Check if Crawlers are still alive
        for crawler in self._crawlers:
            print('Thread ' + crawler.name + ' is Alive? ' + str(crawler.is_alive()))

        # Exit the program
        return

    def get_results(self):
        return self._item_response_strings
