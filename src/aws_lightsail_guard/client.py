import os
import socket
from datetime import datetime

import boto3


class AWSClient:

    def __init__(self):
        self.lightsail = boto3.client('lightsail',
                                      region_name=os.environ['REGION_NAME'],
                                      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    def guard_instance_static_ip_keepalive(self, name):
        instance = self.lightsail.get_instance(instanceName=name)['instance']
        print(f"Check {instance['name']}/{instance['publicIpAddress']}")
        if self.__is_alive(instance['publicIpAddress'], 443):
            print(f"Instance {instance['name']} public static ip {instance['publicIpAddress']} is still alive")
        else:
            print(f"Instance {instance['name']} public static ip {instance['publicIpAddress']} is dead")

            # 创建一个新的静态IP
            new_static_ip_name = "IP-" + datetime.now().strftime("%Y%m%d%H%M%S")
            allocate_static_ip_response = self.lightsail.allocate_static_ip(
                staticIpName=new_static_ip_name
            )
            print(f"Allocate public ip {allocate_static_ip_response} success")

            # 删除老的静态IP
            for static_ip in self.lightsail.get_static_ips()['staticIps']:
                if static_ip['ipAddress'] == instance['publicIpAddress']:
                    try:
                        release_static_ip_response = self.lightsail.release_static_ip(
                            staticIpName=static_ip['name'])
                        print(f"Release public ip {release_static_ip_response} success")
                        break
                    except Exception as e:
                        print(f"Release public ip {release_static_ip_response} fails")

            # 将新建的静态IP绑定到实例上
            attach_static_ip_response = self.lightsail.attach_static_ip(
                staticIpName=new_static_ip_name,
                instanceName=instance['name']
            )
            print(f"Attach public ip {attach_static_ip_response} success")

    def __is_alive(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = (host, port)
        result = sock.connect_ex(location)
        sock.close()
        return result == 0


aws_client = AWSClient()
