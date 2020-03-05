from threading import Thread
from random import randint
import requests
from lxml import html
from HwmsTools import revert


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
    _queue_condition = ''

    def __init__(self, item_, xpaths_, retailer_):
        super().__init__()

        self._item_requested = item_
        self._xpath_name = xpaths_[0]
        self._xpath_price = xpaths_[1]
        self.name = self.name + ' [' + retailer_ + ']'
        # print('Crawler ' + self.name + ' initialised')

    def search(self, queue_, condition_):
        self._queue_to_return = queue_
        self._queue_condition = condition_

        self.find_results()

    def find_results(self):
        print('Crawler \'' + self.name + '\' finding results')
        print('\tUsing queue ' + str(self._result_of_search))

        # !! Do the search at this point !!
        # ToDo: The search
        self.search_for_deals(self._item_requested)

        # Add the found list of items to the list of results
        # self._result_of_search.append([randint(1, 100), randint(100, 200)])

        # Acquire the Queue, add the results, release the Queue
        with self._queue_condition:
            while not self._queue_condition:
                print('Waiting...')
                self._queue_condition.wait()
            else:
                self._queue_to_return.put(self._result_of_search)
                self._queue_condition.notifyAll()

    def search_for_deals(self, search_term):
        print('Initiating Search for: {}'.format(search_term))

        page = requests.get(search_term)
        # print(page.content)

        tree = html.fromstring(page.content)

        print(tree)

        #   Create a list of buyers and prices
        rough_items = tree.xpath(self._xpath_name)
        rough_prices = tree.xpath(self._xpath_price)

        #   Print results
        print('Items: ', rough_items)
        print('Prices: ', rough_prices)
        print('Length of Item list: ', len(rough_items))
        print('Length of Prices list: ', len(rough_prices))

        #   Tidy up the results
        # print('\n')
        refined_items = [x.rstrip() for x in rough_items]
        # refined_prices = [x.strip('[Aa') for x in rough_prices]

        refined_prices = [str(x).replace(".", "") for x in rough_prices]
        refined_prices = [x[:-6] for x in refined_prices]
        refined_prices = [int(x) for x in refined_prices]

        #   Sort both lists without un-linking them
        # refined_prices, refined_items = revert(refined_prices, refined_items)
        # refined_prices = [str(x) for x in refined_prices]

        print('Items: ', refined_items)
        print('Prices: ', refined_prices)
        # self._result_of_search.append([refined_items, refined_prices])

        # return self._result_of_search
