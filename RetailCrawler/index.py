from os import environ
from json import dumps
from multiprocessing import cpu_count

from CrawlerManager import CrawlerManager


def lambda_handler(event, context):
    # Print some things
    print('## ENVIRONMENT')
    print('Environment Vars:\n' + str(environ))
    print('Core Count: ' + str(cpu_count()))
    print('## END ENVIRONMENT\n')

    print('## EVENT')
    print(event)
    print('## END EVENT\n')

    print('## TESTING 01')
    clean_event = str(event).replace("\'", "\"")
    clean_event = str(clean_event).replace("False", "false")
    print('Clean Event:\n' + clean_event)

    cw = CrawlerManager(clean_event)
    cw.load_crawlers()
    print('## END TESTING 01\n')

    print('## TESTING 02')
    sentinel = object()
    for result1 in iter(cw.get_results().get, sentinel):
        for result2 in iter(result1.get, sentinel):
            print('Result: ' + result2)

    print('## END TESTING 02\n')

    # return {
    #     'statusCode': 200,  # OK
    #     'body': dumps('Hello from the first HWMS Lambda Function!')
    # }

    return


# Both of the following functions are for offline testing.  They may be
# required to be disabled for cloud deployment.
# def __main__():
#     new_event = '{ "Records": [ { "eventID": "67aa50f9a78d16d372b673cfec5e6e19", "eventName": "INSERT", ' \
#                 '"eventVersion": "1.1", "eventSource": "aws:dynamodb", "awsRegion": "eu-west-1", "dynamodb": { ' \
#                 '"ApproximateCreationDateTime": 1579040208, "Keys": { "id": { "S": "1579111412732" } }, "NewImage": { '\
#                 '"createdAt": { "S": "2020-01-14T22:16:48.341Z" }, "item": { "S": "CPU Intel i7 9700K" }, ' \
#                 '"__typename": { "S": "SearchQueryRequest" }, "prediction": { "BOOL": false }, "id": { "S": ' \
#                 '"1579111412732" }, "updatedAt": { "S": "2020-01-14T22:16:48.341Z" } }, "SequenceNumber": ' \
#                 '"30337100000000002705939892", "SizeBytes": 157, "StreamViewType": "NEW_AND_OLD_IMAGES" }, ' \
#                 '"eventSourceARN": "arn:aws:dynamodb:eu-west-1:227389701406:table/SearchQueryRequest' \
#                 '-5fsl2xomebd6tmxdjt3xsocctm-testenv/stream/2020-01-08T12:31:34.022" } ] } '
#
#     aws_event = "{'Records': [{'eventID': '67aa50f9a78d16d372b673cfec5e6e19', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-west-1', 'dynamodb': {'ApproximateCreationDateTime': 1579040208, 'Keys': {'id': {'S': '1579111412732'}}, 'NewImage': {'createdAt': {'S': '2020-01-14T22:16:48.341Z'}, 'item': {'S': 'CPU Intel i7 5775C'}, '__typename': {'S': 'SearchQueryRequest'}, 'prediction': {'BOOL': False}, 'id': {'S': '1579111412732'}, 'updatedAt': {'S': '2020-01-14T22:16:48.341Z'}}, 'SequenceNumber': '30337100000000002705939892', 'SizeBytes': 157, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:eu-west-1:227389701406:table/SearchQueryRequest-5fsl2xomebd6tmxdjt3xsocctm-testenv/stream/2020-01-08T12:31:34.022'}]}"
#
#     lambda_handler(aws_event, 'null')
#
#     return
#
#
# if __name__ == '__main__':
#     __main__()
