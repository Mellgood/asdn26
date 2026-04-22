#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import json

ONOS_API = "http://onos:8181/onos/v1/intents"
AUTH = HTTPBasicAuth('onos', 'rocks')
HEADERS = {'Content-Type': 'application/json'}

def create_host_intent(src_mac, dst_mac, app_id="org.onosproject.cli"):
    # Target JSON structure required by ONOS REST API for Host-To-Host capabilities
    intent_json = {
        "type": "HostToHostIntent",
        "appId": app_id,
        "one": src_mac + "/None",  # Append /None explicitly indicating the default VLAN
        "two": dst_mac + "/None"
    }

    print(f"Pushing intent request: {src_mac} <-> {dst_mac} to ONOS...")
    
    # 1. API Call: Example provided using requests.post
    response = requests.post(ONOS_API, auth=AUTH, headers=HEADERS, data=json.dumps(intent_json))
    
    if response.status_code == 201:
        print("Intent successfully calculated and submitted!")
    else:
        print(f"Failed. Error Code: {response.status_code} - {response.text}")

if __name__ == '__main__':
    # MAC addresses mapped in Mininet standard deterministic format
    h1_mac = "00:00:00:00:00:01"
    h3_mac = "00:00:00:00:00:03"
    
    # Executing the pre-made method for h1 -> h3
    create_host_intent(h1_mac, h3_mac)

    # 2. TODO: Establish an Intent identically between h2 and h4!
    h2_mac = "00:00:00:00:00:02"
    h4_mac = "00:00:00:00:00:04"
    # ...
