# Copyright 2023 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
import os
import logging
from datetime import datetime
from aws_lightsail_guard.utils import check_address
from aws_lightsail_guard.lightsail import lightsail, lightsail_domain


class Guard:
    def lightsail_instance_public_ip_keepalive(self, name):
        exist_domains: List[str] = os.environ["DOMAIN_ENTRY_NAME"].split(",")
        max_retries = 3
        for attempt in range(max_retries):
            logging.info(f"Getting instance for {name}")
            instance = lightsail.get_instance(instanceName=name)["instance"]
            old_static_ip = instance["publicIpAddress"]
            if check_address(
                instance["publicIpAddress"], int(os.environ["LIGHTSAIL_INSTANCE_PORT"])
            ):
                logging.info(
                    f"Instance {instance['name']} public static ip {instance['publicIpAddress']} OK"
                )
                get_domains_response = lightsail_domain.get_domains()
                for domain in get_domains_response["domains"]:
                    for entry in domain['domainEntries']:
                        if entry["type"] == 'A' and entry["target"] == instance["publicIpAddress"]:
                            logging.info(f"Domain {entry['name']} public ip {entry['target']} OK")
                return True
            else:
                logging.info(
                    f"Instance {instance['name']} public static ip {instance['publicIpAddress']} ERROR"
                )
                # Allocate new static ip
                new_static_ip = None
                new_static_ip_name = "IP-" + datetime.now().strftime("%Y%m%d%H%M%S")
                allocate_static_ip_response = lightsail.allocate_static_ip(
                    staticIpName=new_static_ip_name
                )
                logging.debug(f"Allocate public ip {allocate_static_ip_response} success")
                # Release others static ip for your memory
                for static_ip in lightsail.get_static_ips()["staticIps"]:
                    if static_ip["name"] == new_static_ip_name:
                        new_static_ip = static_ip["ipAddress"]
                    else:
                        try:
                            release_static_ip_response = lightsail.release_static_ip(
                                staticIpName=static_ip["name"]
                            )
                            logging.debug(
                                f"Release public ip {release_static_ip_response} success"
                            )
                        except Exception as e:
                            logging.error(
                                f"Release public ip fails: {e}"
                            )
                # Attach new static ip to instance
                attach_static_ip_response = lightsail.attach_static_ip(
                    staticIpName=new_static_ip_name, instanceName=instance["name"]
                )
                logging.debug(f"Attach public ip {attach_static_ip_response} success")
                # Update domain entry to new static ip
                get_domains_response = lightsail_domain.get_domains()
                for domain in get_domains_response["domains"]:
                    for entry in domain["domainEntries"]:
                        if entry["type"] == "A" and entry["target"] == old_static_ip:
                            new_entry = entry.copy()
                            new_entry['target'] = new_static_ip
                            lightsail_domain.update_domain_entry(
                                domainName=domain["name"],
                                domainEntry=new_entry,
                            )
                            logging.debug(
                                f"Update domain entry {entry['name']} to {new_static_ip} success"
                            )
                logging.info(
                    f"Instance {instance['name']} public static ip {new_static_ip} RENEWED"
                )
                self.get_lightsail_instance_info(name)
        # If all 3 attempts fail
        logging.error(f"Instance {name} public static ip keepalive failed after {max_retries} attempts.")
        return False

    def get_lightsail_instance_info(self, name):
        instance = lightsail.get_instance(instanceName=name)["instance"]
        static_ips = lightsail.get_static_ips()["staticIps"]
        logging.info("---------- info ----------")
        logging.info(f"name: {instance['name']}")
        logging.info(f"os: {instance['blueprintName']}")
        logging.info(f"public ip: {instance['publicIpAddress']}")
        logging.info("---------- ips -----------")
        for static_ip in static_ips:
            logging.info(
                f"{static_ip['name']}/{static_ip['ipAddress']}/{static_ip['attachedTo']}"
            )
        logging.info("---------- domain --------")
        get_domains_response = lightsail_domain.get_domains()
        for domain in get_domains_response["domains"]:
            for domainEntry in domain["domainEntries"]:
                logging.info(
                    f"{domain['name']}/{domainEntry['name']}/{domainEntry['target']}"
                )


guard = Guard()
