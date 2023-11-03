from aws_lightsail_guard.client import aws_client

if __name__ == '__main__':
    print(aws_client.list_instances())
