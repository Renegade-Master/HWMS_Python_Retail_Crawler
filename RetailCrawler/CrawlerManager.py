from json import loads
from queue import Queue
from threading import Condition

import HwmsTools as hwms
from Crawler import Crawler


class CrawlerManager:
    """ Class: Crawler Manager
    This class handles the Web Crawlers that are created to search for
    the provided RequestString.
    """

    result_list = []
    _result_queue = Queue(len(hwms.Retailer))  # IDE doesn't like this but it works
    wait_for_scrape = Condition()
    _threads = []

    def __init__(self, event_string):
        # Extract the relevant data from the Request
        self.raw_request_string = loads(event_string)
        self._item_requested = (
            self.raw_request_string
            ['Records'][0]['dynamodb']["NewImage"]["item"]["S"]
        )

        # Make a new Crawler for each Retailer
        print('\nInitialising Crawlers...')
        for retailer in hwms.Retailer.__iter__():
            thread = Crawler(
                hwms.format_search_term(self._item_requested, retailer),  # Item requested
                hwms.define_xpath(retailer),  # Item Name and Price XPaths
                retailer  # Retailer name
            )
            thread.setDaemon(True)  # Set Thread to be a Daemon to allow exiting under poor conditions

            self._threads.append(thread)

    def retrieve_search_results(self):
        print('\nBeginning search...')
        for thread in self._threads:
            thread.search(self._result_queue, self.wait_for_scrape)

    def get_results(self):
        # ToDo: Figure out why there are [Crawlers.count] copies of the Queue in the Queue
        # Only return the first item in the Queue to counteract the problem of there being many copies of the queue
        return self._result_queue.queue[0]
