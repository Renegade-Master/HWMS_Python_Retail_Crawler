from threading import Thread
from random import randint


class Crawler(Thread):
    """ Class: Crawler
    This class handles the actual searching of a Search Term on a target
    site.  This Class is intended to be one of many concurrent Crawlers.
    """

    _queue_to_return = ''
    _result_of_search = []
    _item_requested = ''
    _xpath = ''
    _queue_condition = ''

    def __init__(self, item_, xpath_, retailer_):
        super().__init__()

        self._item_requested = item_
        self._xpath = xpath_
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

        # Add the found list of items to the list of results
        self._result_of_search.append([randint(1, 100), randint(100, 200)])

        # Acquire the Queue, add the results, release the Queue
        with self._queue_condition:
            while not self._queue_condition:
                print('Waiting...')
                self._queue_condition.wait()
            else:
                self._queue_to_return.put(self._result_of_search)
                self._queue_condition.notifyAll()
