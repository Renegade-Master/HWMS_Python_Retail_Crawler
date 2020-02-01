#from lxml import html
#import requests
import threading


class Crawler(threading.Thread):
    """ Class: Crawler
    This class handles the actual searching of a Search Term on a target
    site.  This Class is intended to be one of many concurrent Crawlers.
    """

    _item_requested = ''
    _xpath = ''

    def __init__(self, item_, xpath_):
        super().__init__()

        self._item_requested = item_
        self._xpath = xpath_

    def run(self) -> None:
        pass

    def search_for_deals(self, search_term):
        print('Initiating Search for: {}'.format(search_term))

        page = requests.get('https://www.scan.co.uk/search?q={}'.format(search_term))
        tree = html.fromstring(page.content)

        #   Create a list of buyers and prices
        rough_items = tree.xpath('//html/body/div/div/div/div/div/div/div/ul/li/'
                                 'div/span/span[@class="description"]/a/text()')
        rough_prices = tree.xpath('//html/body/div/div/div/div/div/div/div/ul/li/'
                                  'div/div/div/div/span[@class="price"]/text()')

        #   Print results
        # print('Items: ', rough_items)
        # print('Prices: ', rough_prices)
        # print('Length of Item list: ', len(rough_items))
        # print('Length of Prices list: ', len(rough_prices))

        #   Tidy up the results
        # print('\n')
        refined_items = [x.rstrip() for x in rough_items]

        refined_prices = [x[:-1] for x in rough_prices]
        refined_prices = [int(x) for x in refined_prices]

        #   Sort both lists without un-linking them
        refined_prices, refined_items = revert(refined_prices, refined_items)
        refined_prices = [str(x) for x in refined_prices]

        # print('Items: ', refined_items)
        # print('Prices: ', refined_prices)

        return refined_items, refined_prices
