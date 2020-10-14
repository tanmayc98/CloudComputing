import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

# There is some weird stuff in DynamoDB JSON responses. These utils work better.
#from dynamodb_json import json_util as jsond

# There are a couple of types of client.
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIASF6EH44YAI6TUPOZ",
                          aws_secret_access_key="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",
                          region_name='us-east-2')
other_client = boto3.client("dynamodb")

table = dynamodb.Table('FantasyComments')
print("Table = ", table, "\n")


def get_item(table_name, key_value):
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key=key_value
    )

    response = response.get('Item', None)
    return response


def do_a_scan(table_name, filterexpression):
    table = dynamodb.Table(table_name)

    if filterexpression is not None:
        print("Scan with expression")
        response = table.scan(
            FilterExpression=filterexpression
        )
    else:
        response = table.scan(
        )

    print("Scan succeeded")
    #print(json.dumps(response, indent=4))
    return response["Items"]


