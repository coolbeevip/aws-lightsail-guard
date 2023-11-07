import os
import time

import schedule

from aws_lightsail_guard.guard import guard


def job_wrapper():
    guard.lightsail_instance_public_ip_keepalive(name=os.environ['LIGHTSAIL_INSTANCE_NAME'])


if __name__ == '__main__':
    schedule.every(5).minutes.do(job_wrapper)

    while True:
        schedule.run_pending()
        time.sleep(10)
