import logging
import os
import time
from datetime import datetime

import schedule

from aws_lightsail_guard.guard import guard


def job_wrapper():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 24:
        guard.lightsail_instance_public_ip_keepalive(name=os.environ['LIGHTSAIL_INSTANCE_NAME'])
    else:
        logging.info('Skip')


if __name__ == '__main__':
    schedule.every(1).minutes.do(job_wrapper)

    while True:
        schedule.run_pending()
        time.sleep(10)
