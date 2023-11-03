import os

import boto3


class AWSClient:

    def __init__(self):
        self.client = boto3.client('lightsail',
                                   region_name=os.environ['REGION_NAME'],
                                   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    def list_instances(self):
        return self.client.get_instances()


aws_client = AWSClient()
