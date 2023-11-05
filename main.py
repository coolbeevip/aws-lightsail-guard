import os

from aws_lightsail_guard.guard import guard

if __name__ == '__main__':
    guard.lightsail_instance_public_ip_keepalive(name=os.environ['LIGHTSAIL_INSTANCE_NAME'])
