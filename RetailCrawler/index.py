from os import environ
from json import dumps, loads
from multiprocessing import cpu_count
import boto3

from CrawlerManager import CrawlerManager
from HwmsTools import get_current_datetime


def lambda_handler(event, context):
    # Print some things
    # print('## ENVIRONMENT')
    # print('Environment Vars:\n' + str(environ))
    # print('Core Count: ' + str(cpu_count()))
    # print('## END ENVIRONMENT\n')
    #
    # print('## EVENT')
    # print(event)
    # print('## END EVENT\n')

    print('## PHASE 01')
    clean_event = str(event).replace("\'", "\"")
    clean_event = str(clean_event).replace("False", "false")
    # print('Clean Event:\n' + clean_event)

    # Retrieve the RequestID for returning it later
    id = loads(clean_event)['Records'][0]['dynamodb']['Keys']["id"]["S"]

    # Launch the Webcrawlers
    cw = CrawlerManager(clean_event)
    cw.retrieve_search_results()
    print('## END PHASE 01\n')

    print('## PHASE 02')
    # Print the contents of the Queue
    # while not cw.get_results().empty():
    #     temp = cw.get_results().get_nowait()
    #     while temp:
    #         print(temp.pop())

    # [print(x) for x in list(cw.get_results())]
    # print('\nRetailers ')
    # for retailers in list(cw.get_results()):
    #     print(retailers[0])
    #
    # print('\nPrices ')
    # for retailers in list(cw.get_results()):
    #     print(retailers[1])
    #
    # print('\nLinks ')
    # for retailers in list(cw.get_results()):
    #     print(retailers[2])

    print('## END PHASE 02\n')

    # Store the results in a DynamoDB table
    print('## PHASE 03')
    dynamodb = boto3.resource('dynamodb', 'eu-west-1')
    results_table = dynamodb.Table('SearchQueryResponse-5fsl2xomebd6tmxdjt3xsocctm-testenv')

    # Disable the following command to prevent results being posted to DynamoDB
    results_table.put_item(
        Item={
            'id': str(id),
            '__typename': 'SearchQueryResponse',
            'createdAt': get_current_datetime(),
            'result': cw.get_results(),
            'updatedAt': get_current_datetime()
        }
    )

    print('## END PHASE 03\n')

    return {
        'statusCode': 200,  # OK
        'body': dumps('Hello from the first HWMS Lambda Function!')
    }


# Both of the following functions are for offline testing.  They may be
# required to be disabled for cloud deployment.
def __main__():
    aws_event = "{'Records': [{'eventID': '67aa50f9a78d16d372b673cfec5e6e19', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-west-1', 'dynamodb': {'ApproximateCreationDateTime': 1579040208, 'Keys': {'id': {'S': '1579111412732'}}, 'NewImage': {'createdAt': {'S': '2020-01-14T22:16:48.341Z'}, 'item': {'S': 'CPU Intel i5 8600K'}, '__typename': {'S': 'SearchQueryRequest'}, 'prediction': {'BOOL': False}, 'id': {'S': '1579111412732'}, 'updatedAt': {'S': '2020-01-14T22:16:48.341Z'}}, 'SequenceNumber': '30337100000000002705939892', 'SizeBytes': 157, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:eu-west-1:227389701406:table/SearchQueryRequest-5fsl2xomebd6tmxdjt3xsocctm-testenv/stream/2020-01-08T12:31:34.022'}]}"

    lambda_handler(aws_event, 'null')

    return


if __name__ == '__main__':
    __main__()
