import logging
from datetime import datetime

from aws_lightsail_guard.lightsail import lightsail, lightsail_domain
from aws_lightsail_guard.utils import check_address


class Guard:

    def lightsail_instance_public_ip_keepalive(self, name):
        instance = lightsail.get_instance(instanceName=name)['instance']
        # TODO 此处应该检查域名
        if check_address(instance['publicIpAddress'], 443):
            logging.info(
                f"Instance {instance['name']} public static ip {instance['publicIpAddress']} OK")
        else:
            logging.debug(f"Instance {instance['name']} public static ip {instance['publicIpAddress']} ERROR")
            # Allocate new static ip
            new_static_ip = None
            new_static_ip_name = "IP-" + datetime.now().strftime("%Y%m%d%H%M%S")
            allocate_static_ip_response = lightsail.allocate_static_ip(
                staticIpName=new_static_ip_name
            )
            logging.debug(f"Allocate public ip {allocate_static_ip_response} success")

            # Release others static ip
            for static_ip in lightsail.get_static_ips()['staticIps']:
                if static_ip['name'] == new_static_ip_name:
                    new_static_ip = static_ip['ipAddress']
                else:
                    try:
                        release_static_ip_response = lightsail.release_static_ip(
                            staticIpName=static_ip['name'])
                        logging.info(f"Release public ip {release_static_ip_response} success")
                    except Exception as e:
                        logging.info(f"Release public ip {release_static_ip_response} fails")

            # Attach new static ip to instance
            attach_static_ip_response = lightsail.attach_static_ip(
                staticIpName=new_static_ip_name,
                instanceName=instance['name']
            )
            logging.debug(f"Attach public ip {attach_static_ip_response} success")

            # Update domain entry to new static ip
            get_domains_response = lightsail_domain.get_domains()
            for domain in get_domains_response['domains']:
                for domainEntry in domain['domainEntries']:
                    if domainEntry['target'] == 't5.coolbeevip.com':
                        lightsail_domain.update_domain_entry(
                            domainName=domain['name'],
                            domainEntry={
                                'id': domainEntry['id'],
                                'name': domainEntry['name'],
                                'target': new_static_ip,
                                'type': domainEntry['type'],
                            }
                        )
                        logging.debug(f"Update domain entry {domainEntry['name']} to {new_static_ip} success")
            logging.info(
                f"Instance {instance['name']} public static ip {new_static_ip} RENEWED")
            self.get_lightsail_instance_info(name)

    def get_lightsail_instance_info(self, name):
        instance = lightsail.get_instance(instanceName=name)['instance']
        static_ips = lightsail.get_static_ips()['staticIps']
        logging.info(f"---------- info ----------")
        logging.info(f"name: {instance['name']}")
        logging.info(f"os: {instance['blueprintName']}")
        logging.info(f"public ip: {instance['publicIpAddress']}")
        logging.info(f"---------- ips -----------")
        for static_ip in static_ips:
            logging.info(f"{static_ip['name']}/{static_ip['ipAddress']}/{static_ip['attachedTo']}")
        logging.info(f"---------- domain --------")
        get_domains_response = lightsail_domain.get_domains()
        for domain in get_domains_response['domains']:
            for domainEntry in domain['domainEntries']:
                logging.info(f"{domain['name']}/{domainEntry['name']}/{domainEntry['target']}")


guard = Guard()
