from enum import Enum
from re import compile, IGNORECASE
from lxml import html


#   Function for sorting two lists by one of the lists, but retaining the order of the second list
def revert(a, b):
    a, b = map(list, zip(*sorted(zip(a, b), key=lambda x: x[0])))
    return a, b


def format_search_term(item_, retailer_):
    """ Function: format_search_term
    This function is used to convert a provided Item, and create a
    URL to a store page.
    """

    repl = ''
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
    # ToDo: Move the retailer specific Strings to an external file
    #  that is read in
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
            '//span[@class="price"]/text()']
    elif retailer_ == Retailer.NO_KOMPLETT:
        x_paths = [
            '//span[@itemprop="name"]/text()',
            '//div[@class="productlist-huidigeprijs"]/text()']
    # elif retailer_ == Retailer.UK_AMAZON:
    #     x_paths = \
    #         '/html/body/div[1]/div[2]/div[1]/div[2]/div/span[4]/div[1]/div[3]/div/span/div/div/div[2]/div[2]/div/div[' \
    #         '1]/div/div/div[1]/h2/a/span '
    elif retailer_ == Retailer.UK_ARIA:
        x_paths = [
            '//tr[@class="listTableTrSS"]/td[@style="max-width: 350px;"]/strong/a/text()',
            '//span[@class="price bold"]/text()']
    elif retailer_ == Retailer.UK_SCAN:
        x_paths = [
            '//span[@class="description"]/a/text()',
            '//div[@class="leftColumn"]/span[@class="price"]/text()']

    # print('XPath: ' + x_paths)
    return x_paths


def clean_price_results(retailer_, price_list_):
    """ Function: clean_price_results
    This function takes the raw scraped data and cleans it according to the Retailer from which the data originated.
    """

    cleaned_price_list = ''

    # if retailer_ == Retailer.DE_AMAZON:
    #     pass
    if retailer_ == Retailer.DE_CASEKING:
        pass
    elif retailer_ == Retailer.NO_KOMPLETT:
        pass
    # elif retailer_ == Retailer.UK_AMAZON:
    #     pass
    elif retailer_ == Retailer.UK_ARIA:
        pass
    elif retailer_ == Retailer.UK_SCAN:
        pass

    print('Cleaned Price List: ' + cleaned_price_list)
    return cleaned_price_list


def clean_product_name_results(retailer_, title_list_):
    """ Function: clean_product_name_results
    This function takes the raw scraped data and cleans it according to the Retailer from which the data originated.
    """

    cleaned_product_name_list = ''

    # if retailer_ == Retailer.DE_AMAZON:
    #     pass
    if retailer_ == Retailer.DE_CASEKING:
        pass
    elif retailer_ == Retailer.NO_KOMPLETT:
        pass
    # elif retailer_ == Retailer.UK_AMAZON:
    #     pass
    elif retailer_ == Retailer.UK_ARIA:
        pass
    elif retailer_ == Retailer.UK_SCAN:
        pass

    print('Cleaned Product Name List: ' + cleaned_product_name_list)
    return cleaned_product_name_list


class Retailer(Enum):
    """ Enum: Retailer
    Enum to branch execution path based on different Retailers.
    """
    # DE_AMAZON = 0
    DE_CASEKING = 1
    NO_KOMPLETT = 2
    # UK_AMAZON = 3
    UK_ARIA = 4
    UK_SCAN = 5
