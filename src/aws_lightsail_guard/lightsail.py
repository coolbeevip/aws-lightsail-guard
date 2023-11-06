import os

import boto3

lightsail = boto3.client('lightsail',
                         region_name=os.environ['REGION_NAME'],
                         aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                         aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

lightsail_domain = boto3.client('lightsail',
                                region_name='us-east-1',
                                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
