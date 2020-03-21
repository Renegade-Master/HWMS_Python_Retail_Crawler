#  Copyright (c) 2020 RenegadeMaster Inc. - All Right Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  The contents of this file are proprietary and confidential.
#  Written by Ciaran Bent <ciaran.bent@protonmail.ch>, March 2020

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

    result_list = [[], [], []]
    _result_queue = Queue(len(hwms.Retailer))  # IDE doesn't like this but it works
    wait_for_scrape = Condition()
    _threads = []

    def __init__(self, event_string):
        """ Function: __init__
        Initialise the CrawlerManager Class with the request String
        """

        # Extract the relevant data from the Request
        raw_request_string = loads(event_string)
        _item_requested = (
            raw_request_string
            ['Records'][0]['dynamodb']["NewImage"]["item"]["S"]
        )

        # Make a new Crawler for each Retailer
        # print('\nInitialising Crawlers...')
        for retailer in hwms.Retailer.__iter__():
            thread = Crawler(
                hwms.format_search_term(_item_requested, retailer),  # Item requested
                hwms.define_xpath(retailer),  # Item XPaths
                retailer  # Retailer name
            )

            # Set Thread to be a Daemon to allow exiting under poor conditions
            thread.setDaemon(True)

            self._threads.append(thread)

    def retrieve_search_results(self):
        """ Function: retrieve_search_results
        Send the Web-Crawlers off to find results
        """
        # print('\nBeginning search...')
        for thread in self._threads:
            thread.search(self._result_queue, self.wait_for_scrape)

    def get_results(self):
        """ Function: get_results
        Combine and return all results from the Web-Crawl into one large list
        """
        # ToDo: Figure out why there are [Crawlers.count] copies of the Queue in the Queue
        # Only operate on the first item in the Queue to counteract the problem of there being many copies of the queue

        # Add the Title fields
        for retailer in self._result_queue.queue[0][0]:
            for title in retailer:
                self.result_list[0].append(title)

        # Add the Price fields
        for retailer in self._result_queue.queue[0][1]:
            for price in retailer:
                self.result_list[1].append(price)

        # Add the Link fields
        for retailer in self._result_queue.queue[0][2]:
            for link in retailer:
                self.result_list[2].append(link)

        # Sort the new Master List
        self.result_list[1], self.result_list[0], self.result_list[2] = (
            hwms.sort_set_retaining_order(self.result_list[1], self.result_list[0], self.result_list[2]))

        # Return the List
        return self.result_list
