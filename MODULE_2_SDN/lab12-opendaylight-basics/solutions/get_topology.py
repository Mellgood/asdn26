#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import json

ODL_API = "http://opendaylight:8181/restconf/operational/network-topology:network-topology"
AUTH = HTTPBasicAuth('admin', 'admin')

def fetch_topology():
    print("Querying OpenDaylight RESTCONF API...")
    
    try:
        response = requests.get(ODL_API, auth=AUTH)
        
        if response.status_code == 200:
            topology_data = response.json()
            
            # Extract the actual nodes list from the deeply nested RESTCONF YANG tree
            nodes = topology_data['network-topology']['topology'][0]['node']
            
            print(f"Success! Total nodes dynamically discovered by ODL: {len(nodes)}")
            
        else:
            print(f"Failed. HTTP Error Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Connection failed. Is the ODL container fully booted and are the Karaf features installed?")

if __name__ == '__main__':
    fetch_topology()
