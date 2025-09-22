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

import json
import os
import time
from datetime import datetime, timedelta

import schedule

from aws_lightsail_guard.guard import guard

COOLDOWN_FILE = 'logs/cooldown_state.json'
COOLDOWN_HOURS = 12
MAX_FAILS = 3


def load_cooldown_state():
    try:
        with open(COOLDOWN_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {"fail_count": 0, "cooldown_until": None}


def save_cooldown_state(state):
    with open(COOLDOWN_FILE, 'w') as f:
        json.dump(state, f)


def job_wrapper():
    state = load_cooldown_state()
    now = datetime.now()
    cooldown_until = None
    if state.get("cooldown_until"):
        cooldown_until = datetime.fromisoformat(state["cooldown_until"])
    if cooldown_until and now < cooldown_until:
        print(f"In cooldown until {cooldown_until}, skipping job.")
        return
    result = guard.lightsail_instance_public_ip_keepalive(name=os.environ['LIGHTSAIL_INSTANCE_NAME'])
    if result:
        state["fail_count"] = 0
        state["cooldown_until"] = None
    else:
        state["fail_count"] = state.get("fail_count", 0) + 1
        if state["fail_count"] >= MAX_FAILS:
            state["cooldown_until"] = (now + timedelta(hours=COOLDOWN_HOURS)).isoformat()
            print(f"Failed {MAX_FAILS} times, entering cooldown until {state['cooldown_until']}")
    save_cooldown_state(state)


if __name__ == '__main__':
    schedule.every(5).minutes.do(job_wrapper)

    while True:
        schedule.run_pending()
        time.sleep(10)
