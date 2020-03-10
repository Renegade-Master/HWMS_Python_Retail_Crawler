from enum import Enum
from re import compile, IGNORECASE
from datetime import datetime
from decimal import Decimal

""" Script: HwmsTools
This script is a container for various helper functions required by one
or more of the Classes used in the Web-Crawling functionality of HWMS.
"""


def sort_set_retaining_order(a, b, c):
    """ Function: revert
    This function sorts three lists by a key comprised of items in the
     first list, while retaining the relative order of the other lists.

    """
    if len(a) == 0:
        return a, b, c

    a, b, c = map(list, zip(*sorted(zip(a, b, c), key=lambda x: x[0])))
    return a, b, c


def get_current_datetime():
    """ Function: get_current_datetime
    This function returns the current Date-Time in the same format that
    is used by the AWS DynamoDB.
    """
    timestamp = str(datetime.now())
    timestamp = timestamp.replace(" ", "T")
    timestamp = timestamp[:-3]
    timestamp += 'Z'
    return timestamp


def format_search_term(item_, retailer_):
    """ Function: format_search_term
    This function is used to convert a provided Item, and create a
    URL to a store page.
    """

    regex = compile(r'\s', IGNORECASE)  # Look for spaces to replace

    # Format the term however the Retailer is expecting
    # if (retailer_ == Retailer.DE_AMAZON or
    #         retailer_ == Retailer.DE_CASEKING or
    #         retailer_ == Retailer.NO_KOMPLETT or
    #         retailer_ == Retailer.UK_AMAZON or
    #         retailer_ == Retailer.UK_ARIA or
    #         retailer_ == Retailer.UK_SCAN):
    #     repl = '+'
    # else:
    #     raise ValueError('CrawlerManager._format_search_term: '
    #                      'Unsupported or missing value provided for'
    #                      ' Retailer.')

    repl = '+'
    clean_string = regex.sub(repl, item_)

    # Format the search URL.
    search_url = ''

    # if retailer_ == Retailer.DE_AMAZON:
    #     search_url = \
    #         'https://www.amazon.de/s?k={0}' \
    #         .format(clean_string)
    if retailer_ == Retailer.DE_CASEKING:
        search_url = \
            'https://www.caseking.de/search?sSearch={0}' \
                .format(clean_string)
    elif retailer_ == Retailer.NO_KOMPLETT:
        search_url = \
            'https://www.komplett.ie/search-results/?tn_q={0}' \
                .format(clean_string)
    # elif retailer_ == Retailer.UK_AMAZON:
    #     search_url = \
    #         'https://www.amazon.co.uk/s?k={0}' \
    #         .format(clean_string)
    elif retailer_ == Retailer.UK_ARIA:
        search_url = \
            'https://www.aria.co.uk/Products?search={0}' \
                .format(clean_string)
    elif retailer_ == Retailer.UK_SCAN:
        search_url = \
            'https://www.scan.co.uk/search?q={0}' \
                .format(clean_string)

    # print('Search URL: ' + search_url)
    return search_url


def define_xpath(retailer_):
    """ Function: define_xpath
    This function is used to create the XPath to the price data of
    different retailers.
    """

    x_paths = ''

    # if retailer_ == Retailer.DE_AMAZON:
    #     x_paths = \
    #         '/html/body/div[1]/div[1]/div[1]/div[2]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[2]/div/div[' \
    #         '1]/div/div/div[1]/h2/a/span'

    if retailer_ == Retailer.DE_CASEKING:
        x_paths = [
            '//span[@class="ProductTitle"]/text()',
            '//span[@class="price"]/text()',
            '//div[@class="overlay"]/a[@class="more"]']

    elif retailer_ == Retailer.NO_KOMPLETT:
        x_paths = [
            '//span[@itemprop="name"]/text()',
            '//div[@class="productlist-huidigeprijs"]/text()',
            '//div[@class="col-sm-3 productitem-image"]/a[@itemprop="url"]']

    # elif retailer_ == Retailer.UK_AMAZON:
    #     x_paths = \
    #         '/html/body/div[1]/div[2]/div[1]/div[2]/div/span[4]/div[1]/div[3]/div/span/div/div/div[2]/div[2]/div/div[' \
    #         '1]/div/div/div[1]/h2/a/span '

    elif retailer_ == Retailer.UK_ARIA:
        x_paths = [
            '//tr[@class="listTableTrSS"]/td[@style="max-width: 350px;"]/strong/a/text()',
            '//span[@class="price bold"]/text()',
            '//tr[@class="listTableTrSS"]/td[@style="max-width: 350px;"]/strong/a']

    elif retailer_ == Retailer.UK_SCAN:
        x_paths = [
            '//span[@class="description"]/a/text()',
            '//div[@class="leftColumn"]/span[@class="price"]/text()',
            '//span[@class="description"]/a']

    # print('XPath: ' + x_paths)
    return x_paths


def clean_price_results(retailer_, price_list_):
    """ Function: clean_price_results
    This function takes the raw scraped Price data and cleans
    it according to the Retailer from which the data originated.

    Will require a way to convert Currency eventually as
    both GBP and EUR are returned.
    """

    # ToDo: Add currency conversion for any price not in EUR.  For now,
    #  just remove currency symbol
    cleaned_price_list = ''
    Decimal(2)

    # if retailer_ == Retailer.DE_AMAZON:
    #     pass

    if retailer_ == Retailer.DE_CASEKING:
        price_list_ = [x[:-3] for x in price_list_]
        price_list_ = [str(x).replace(".", "") for x in price_list_]
        cleaned_price_list = [str(x).replace(",", ".") for x in price_list_]
        # cleaned_price_list = [str('€' + x) for x in price_list_]

    elif retailer_ == Retailer.NO_KOMPLETT:
        price_list_ = [str(x).replace(",", "") for x in price_list_]
        cleaned_price_list = [str(x).replace("-", "00") for x in price_list_]
        # cleaned_price_list = [str('€' + x) for x in price_list_]

    # elif retailer_ == Retailer.UK_AMAZON:
    #     pass

    elif retailer_ == Retailer.UK_ARIA:
        cleaned_price_list = [str(x).replace("£", "") for x in price_list_]
        # cleaned_price_list = price_list_

    elif retailer_ == Retailer.UK_SCAN:
        cleaned_price_list = [str(x + '99') for x in price_list_]
        # cleaned_price_list = [str('£' + x) for x in price_list_]

    cleaned_price_list = [Decimal(x) for x in cleaned_price_list]

    return cleaned_price_list


def clean_title_results(retailer_, title_list_):
    """ Function: clean_product_name_results
    This function takes the raw scraped Title data and cleans
    it according to the Retailer from which the data originated.
    """

    cleaned_product_name_list = ''

    # Remove leading and trailing whitespace
    title_list_ = [x.lstrip() for x in title_list_]
    title_list_ = [x.rstrip() for x in title_list_]

    # if retailer_ == Retailer.DE_AMAZON:
    #     pass

    if retailer_ == Retailer.DE_CASEKING:
        cleaned_product_name_list = title_list_

    elif retailer_ == Retailer.NO_KOMPLETT:
        title_list_ = [x.strip('\r') for x in title_list_]
        cleaned_product_name_list = [x.strip('\n') for x in title_list_]

    # elif retailer_ == Retailer.UK_AMAZON:
    #     pass

    elif retailer_ == Retailer.UK_ARIA:
        cleaned_product_name_list = title_list_

    elif retailer_ == Retailer.UK_SCAN:
        cleaned_product_name_list = title_list_

    return cleaned_product_name_list


def clean_link_results(retailer_, link_list_):
    """ Function: clean_link_results
    This function takes the raw scraped URL data and cleans
    it according to the Retailer from which the data originated.
    """

    cleaned_link_list_ = ''

    # if retailer_ == Retailer.DE_AMAZON:
    #     pass

    if retailer_ == Retailer.DE_CASEKING:
        cleaned_link_list_ = [
            x.attrib['href']
            for x in link_list_]

    elif retailer_ == Retailer.NO_KOMPLETT:
        cleaned_link_list_ = [
            str('https://www.komplett.ie' + x.attrib['href'])
            for x in link_list_]

    # elif retailer_ == Retailer.UK_AMAZON:
    #     pass

    elif retailer_ == Retailer.UK_ARIA:
        cleaned_link_list_ = [
            str('https://www.aria.co.uk' + x.attrib['href'])
            for x in link_list_]

    elif retailer_ == Retailer.UK_SCAN:
        cleaned_link_list_ = [
            str('https://www.scan.co.uk' + x.attrib['href'])
            for x in link_list_]

    return cleaned_link_list_


class Retailer(Enum):
    """ Enum: Retailer
    Enum to branch execution path based on different Retailers.
    """
    DE_CASEKING = 0
    NO_KOMPLETT = 1
    UK_ARIA = 2
    UK_SCAN = 3
    # DE_AMAZON = 4
    # UK_AMAZON = 5
