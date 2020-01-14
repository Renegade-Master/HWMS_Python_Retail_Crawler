import json
import os


def lambda_handler(event, context):
    # TODO: implement

    # Print some things
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## EVENT')
    print(event)

    return {
        'statusCode': 200,  # OK
        'body': json.dumps('Hello from the first HWMS Lambda Function!')

    }
