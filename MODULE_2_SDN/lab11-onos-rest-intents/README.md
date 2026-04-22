# Lab 11: ONOS REST API & "Intents"

A key architecture of modern SDN controllers is their external Northbound Interface (NBI), highly standardized via robust REST APIs.

Instead of meticulously constructing `OFPFlowMod` byte-level rules locally as we did in Ryu, ONOS allows you to dictate **Intents**. An *Intent* is a high-level policy (e.g., "I want Host 1 to be able to talk to Host 3"). ONOS automatically calculates the shortest path (using Dijkstra algorithm internally) and cascades the correct low-level `FlowMod` rules to all required intermediate switches underneath without you micromanaging them.

## Topology
Same Ring-4 topology as Lab 10. Start the fresh environment:
```bash
docker compose up -d
docker exec -it asdn_mininet_lab11 /bin/bash
```

*Note: In this lab, we mapped an environment variable to explicitly **disable** the automatic `fwd` reactive routing app (`org.onosproject.fwd`). Because of this, the network will NOT route anything by default. `pingall` will silently fail!*

## Tasks

### Task 1: Bootstrap the Host identifiers
1. Inside the Mininet container, start the topology: `mn --topo ring,4 --controller=remote,ip=onos,port=6653`.
2. In Mininet, do a `pingall`. It will absolutely fail natively, but the packets hitting the ingress switches will be sent as `PACKET_IN` up to ONOS. Even without a routing app, ONOS learns the existence of the hosts from these orphans.
3. ONOS tracks hosts by their MAC address + VLAN tuple (e.g., `00:00:00:00:00:01/None`). Test this by checking the GUI (`http://localhost:8181/onos/ui`).

### Task 2: Push Intents via API
1. Open the starter script `intent_maker.py`. We will use the Python `requests` HTTP library to act as an external orchestration application.
2. We provided a working example of structuring JSON to POST a `HostToHostIntent` from Host 1 to Host 3 to the `/onos/v1/intents` endpoint.
3. Complete the `TODO` to formulate a secondary script action pushing an intent between `h2` and `h4`.
4. From inside the Mininet container (Terminal 2), run the script:
   ```bash
   python3 /lab/intent_maker.py
   ```
5. Go back to Mininet and try `h1 ping h3` and `h2 ping h4`. They should now magically work due to the active intents calculated by ONOS!
