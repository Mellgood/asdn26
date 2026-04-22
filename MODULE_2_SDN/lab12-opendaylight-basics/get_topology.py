#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import json

# ODL RESTCONF endpoint for network topology (Operational Data Store)
ODL_API = "http://opendaylight:8181/restconf/operational/network-topology:network-topology"
AUTH = HTTPBasicAuth('admin', 'admin')

def fetch_topology():
    print("Querying OpenDaylight RESTCONF API...")
    
    try:
        # 1. API Call: Example provided for fetching data via GET
        response = requests.get(ODL_API, auth=AUTH)
        
        if response.status_code == 200:
            topology_data = response.json()
            
            # 2. Extract Data
            # TODO: Extract the list of "node" elements from the loaded JSON
            # Hint: The nested dictionary path is:
            # topology_data['network-topology']['topology'][0]['node']
            
            nodes = [] # Replace this empty list with the correct JSON extraction path!
            
            print(f"Success! Total nodes dynamically discovered by ODL: {len(nodes)}")
            
            # Print the entire JSON (Optional, can be overwhelming)
            # print(json.dumps(topology_data, indent=4))
        else:
            print(f"Failed. HTTP Error Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Connection failed. Is the ODL container fully booted and are the Karaf features installed?")

if __name__ == '__main__':
    fetch_topology()
