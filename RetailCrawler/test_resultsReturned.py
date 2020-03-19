from CrawlerManager import CrawlerManager


def test_results_are_returned():
    aws_event = "{'Records': [{'eventID': '67aa50f9a78d16d372b673cfec5e6e19', 'eventName': 'INSERT', 'eventVersion': " \
                "'1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-west-1', 'dynamodb': {" \
                "'ApproximateCreationDateTime': 1579040208, 'Keys': {'id': {'S': '1111111111111'}}, 'NewImage': {" \
                "'createdAt': {'S': '2020-01-14T22:16:48.341Z'}, 'item': {'S': 'CPU Intel i5 8600K'}, '__typename': {" \
                "'S': 'SearchQueryRequest'}, 'prediction': {'BOOL': False}, 'id': {'S': '1579111412732'}, " \
                "'updatedAt': {'S': '2020-01-14T22:16:48.341Z'}}, 'SequenceNumber': '30337100000000002705939892', " \
                "'SizeBytes': 157, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': " \
                "'arn:aws:dynamodb:eu-west-1:227389701406:table/SearchQueryRequest-5fsl2xomebd6tmxdjt3xsocctm-testenv" \
                "/stream/2020-01-08T12:31:34.022'}]} "

    clean_event = str(aws_event).replace("\'", "\"")
    clean_event = str(clean_event).replace("False", "false")

    cw = CrawlerManager(clean_event)
    cw.retrieve_search_results()

    assert cw.get_results() != ''
