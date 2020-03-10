from threading import Thread

import requests
from lxml import html

from HwmsTools import clean_price_results, clean_title_results,\
    clean_link_results, sort_set_retaining_order


class Crawler(Thread):
    """ Class: Crawler
    This class handles the actual searching of a Search Term on a target
    site.  This Class is intended to be one of many concurrent Crawlers.
    """

    _queue_to_return = ''
    _result_of_search = [[], [], []]
    _item_requested = ''
    _xpath_price = ''
    _xpath_name = ''
    _xpath_item_link = ''
    _queue_condition = ''
    _retailer = ''

    def __init__(self, item_, xpaths_, retailer_):
        """ Function: __init__
        Initialisation function for the Crawler Class.  Loads up the
        Crawler with the data required to scrape a particular retailer.
        """
        super().__init__()

        self._item_requested = item_
        self._xpath_name = xpaths_[0]
        self._xpath_price = xpaths_[1]
        self._xpath_item_link = xpaths_[2]
        self._retailer = retailer_
        self.name = self.name + ' [' + str(retailer_) + ']'
        print('Crawler ' + self.name + ' initialised')

    def search(self, queue_, condition_):
        """ Function: search
        Activate the Web-Crawler.  Serves essentially as a wrapper for
        the `run()` function.
        """

        self._queue_to_return = queue_
        self._queue_condition = condition_

        self.find_results()

    def find_results(self):
        """ Function find_results
        Handle the Crawler's interaction with the Results Queue, ensuring
        that it does not corrupt or become blocked.
        """

        # print('Crawler \'' + self.name + '\' finding results')
        # print('\tUsing queue ' + str(self._result_of_search))

        # Scrape and clean the current price data
        self.search_for_deals(self._item_requested)

        # Acquire the Queue, add the results, release the Queue
        with self._queue_condition:
            while not self._queue_condition:
                print('Waiting...')
                self._queue_condition.wait()
            else:
                self._queue_to_return.put(self._result_of_search)
                self._queue_condition.notifyAll()

    def search_for_deals(self, search_term):
        """ Function: search_for_deals
        Search the provided URL for items relating to the Search Term.
        """
        # print('Initiating Search for: {}'.format(search_term))

        raw_page_data = requests.get(search_term)
        # print(raw_page_data.content)

        page_html_tree = html.fromstring(raw_page_data.content)

        #   Create a list of buyers and prices
        rough_items = page_html_tree.xpath(self._xpath_name)
        rough_prices = page_html_tree.xpath(self._xpath_price)
        rough_links = page_html_tree.xpath(self._xpath_item_link)

        #   Print results
        # print('Rough Items: ', rough_items)
        # print('Rough Prices: ', rough_prices)

        # print('Length of Item list: ', len(rough_items))
        # print('Length of Prices list: ', len(rough_prices))
        # print('Length of Links list: ', len(rough_links))

        #   Tidy up the results
        refined_items = clean_title_results(self._retailer, rough_items)
        refined_prices = clean_price_results(self._retailer, rough_prices)
        refined_links = clean_link_results(self._retailer, rough_links)

        # Sort the items according to Price without losing relative ordering
        refined_prices, refined_items, refined_links = (
            sort_set_retaining_order(refined_prices, refined_items, refined_links))

        # Print the Results
        # print('Clean Items: ', refined_items)
        # print('Clean Prices: ', refined_prices)
        # print('Clean Links: ', refined_links)
        # print('\n---\n')

        self._result_of_search[0].append(refined_items)
        self._result_of_search[1].append(refined_prices)
        self._result_of_search[2].append(refined_links)
