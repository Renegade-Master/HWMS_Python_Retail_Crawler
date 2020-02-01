import os
import json

import CrawlerManager


def lambda_handler(event, context):
    # TODO: implement

    # Print some things
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## END ENVIRONMENT VARIABLES')

    print('## EVENT')
    print(event)
    print('## END EVENT')

    print('## TESTING 01')
    cw = CrawlerManager.CrawlerManager(event)
    print(cw.load_crawlers())
    print('## END TESTING 01')

    return {
        'statusCode': 200,  # OK
        'body': json.dumps('Hello from the first HWMS Lambda Function!')
    }
