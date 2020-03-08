from threading import Thread

import requests
from lxml import html

from HwmsTools import clean_price_results, clean_title_results,\
    clean_link_results, sort_retaining_order


class Crawler(Thread):
    """ Class: Crawler
    This class handles the actual searching of a Search Term on a target
    site.  This Class is intended to be one of many concurrent Crawlers.
    """

    _queue_to_return = ''
    _result_of_search = []
    _item_requested = ''
    _xpath_price = ''
    _xpath_name = ''
    _xpath_item_link = ''
    _queue_condition = ''
    _retailer = ''

    def __init__(self, item_, xpaths_, retailer_):
        super().__init__()

        self._item_requested = item_
        self._xpath_name = xpaths_[0]
        self._xpath_price = xpaths_[1]
        self._xpath_item_link = xpaths_[2]
        self._retailer = retailer_
        self.name = self.name + ' [' + str(retailer_) + ']'
        print('Crawler ' + self.name + ' initialised')

    def search(self, queue_, condition_):
        self._queue_to_return = queue_
        self._queue_condition = condition_

        self.find_results()

    def find_results(self):
        # print('Crawler \'' + self.name + '\' finding results')
        # print('\tUsing queue ' + str(self._result_of_search))

        # Scrape and clean the current price data
        self.search_for_deals(self._item_requested)

        # Add the found list of items to the list of results

        # Acquire the Queue, add the results, release the Queue
        with self._queue_condition:
            while not self._queue_condition:
                print('Waiting...')
                self._queue_condition.wait()
            else:
                self._queue_to_return.put(self._result_of_search)
                self._queue_condition.notifyAll()

    def search_for_deals(self, search_term):
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

        #   Sort the lists without un-linking them
        # refined_prices, refined_links = revert(refined_prices, refined_links)
        # refined_prices, refined_items = revert(refined_prices, refined_items)
        refined_prices, refined_items, refined_links = (
            sort_retaining_order(refined_prices, refined_items, refined_links))
        # refined_prices = [str(x) for x in refined_prices]

        # Print the Results
        # print('Clean Items: ', refined_items)
        # print('Clean Prices: ', refined_prices)
        # print('Clean Links: ', refined_links)
        # print('Clean Links: ')
        # [print('\t', x) for x in refined_links]
        # print('\n---\n')

        self._result_of_search.append([refined_items, refined_prices, refined_links])
