import os

from aws_lightsail_guard.client import aws_client

if __name__ == '__main__':
    aws_client.guard_instance_static_ip_keepalive(name=os.environ['LIGHTSAIL_INSTANCE_NAME'])
