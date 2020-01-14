import json


def lambda_handler(event, context):
    # TODO: implement
    return {
        'statusCode': 200,  # OK
        'body': json.dumps('Hello from the first HWMS Lambda Function!')
    }
