from datetime import datetime

from aws_lightsail_guard.lightsail import lightsail
from aws_lightsail_guard.utils import check_address


class Guard:

    def lightsail_instance_public_ip_keepalive(self, name):
        instance = lightsail.get_instance(instanceName=name)['instance']
        print(f"Check {instance['name']}/{instance['publicIpAddress']}")
        if check_address(instance['publicIpAddress'], 443):
            print(f"Instance {instance['name']} public static ip {instance['publicIpAddress']} is still alive")
        else:
            print(f"Instance {instance['name']} public static ip {instance['publicIpAddress']} is dead")

            # Allocate new static ip
            new_static_ip_name = "IP-" + datetime.now().strftime("%Y%m%d%H%M%S")
            allocate_static_ip_response = lightsail.allocate_static_ip(
                staticIpName=new_static_ip_name
            )
            print(f"Allocate public ip {allocate_static_ip_response} success")

            # Release old static ip
            for static_ip in lightsail.get_static_ips()['staticIps']:
                if static_ip['ipAddress'] == instance['publicIpAddress']:
                    try:
                        release_static_ip_response = lightsail.release_static_ip(
                            staticIpName=static_ip['name'])
                        print(f"Release public ip {release_static_ip_response} success")
                        break
                    except Exception as e:
                        print(f"Release public ip {release_static_ip_response} fails")

            # Attach new static ip to instance
            attach_static_ip_response = lightsail.attach_static_ip(
                staticIpName=new_static_ip_name,
                instanceName=instance['name']
            )
            print(f"Attach public ip {attach_static_ip_response} success")


guard = Guard()
