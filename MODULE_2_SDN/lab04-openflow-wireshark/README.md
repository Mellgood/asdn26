# Lab 04: Uncovering OpenFlow with Wireshark & tshark

In this lab, you will peek "under the hood" of the OpenFlow protocol. SDN is governed by the communication between the Data Plane (Switch) and the Control Plane (Controller). We will use packet sniffing tools to capture and analyze the exact messages exchanged during network initialization and host events.

## Setup
Start your lab environment:
```bash
docker compose up -d
docker exec -it asdn_mininet_lab04 /bin/bash
```

## Tasks

### Task 1: Start the Packet Capture
We will use `tshark` (the command-line version of Wireshark) inside the container to capture traffic on the loopback interface (`lo`). The OpenFlow controller and the virtual switches typically communicate locally on port `6633` or `6653`.

1. In your **first terminal** (inside the container), start a capture filtering for OpenFlow traffic and save it to a file:
   ```bash
   tshark -i lo -f "tcp port 6653 or tcp port 6633" -w /lab/openflow_capture.pcap
   ```
   *(Leave this running in the foreground)*

### Task 2: Trigger OpenFlow Traffic
1. Open a **second terminal window** on your host and attach to the container:
   ```bash
   docker exec -it asdn_mininet_lab04 /bin/bash
   ```
2. Start Mininet with the default topology. Mininet automatically spins up a default reference controller on localhost.
   ```bash
   mn
   ```
3. Once Mininet creates the network, wait a few seconds, then trigger an ICMP ping from `h1` to `h2`:
   ```bash
   mininet> h1 ping -c 1 h2
   ```
4. Exit Mininet cleanly by typing `exit`.
5. Go back to your **first terminal** and stop the `tshark` capture using `Ctrl+C`.

### Task 3: Analyze the Capture
You now have a `.pcap` file located at `MODULE_2_SDN/lab04-openflow-wireshark/openflow_capture.pcap` on your host machine (thanks to the Docker volume mount).

1. Open this `.pcap` file on your host machine using the **Wireshark GUI** (if installed locally). This is highly recommended for readability.
   Alternatively, read it directly inside the container using `tshark`:
   ```bash
   tshark -r /lab/openflow_capture.pcap -V -Y "openflow_v1 or openflow_v4" | less
   ```

2. Scrutinize the packets. Try to locate and inspect the fields of the following core OpenFlow messages:
   - **HELLO**: The initial handshake between the switch and the controller. What version of OpenFlow was negotiated?
   - **FEATURES_REQUEST / FEATURES_REPLY**: The controller asking the switch for its hardware capabilities (e.g., Datapath ID, port list).
   - **PACKET_IN**: Investigate this payload. When `h1` pinged `h2`, the switch didn't know the MAC address. It encapsulated the ARP/ICMP packet inside an OpenFlow `PACKET_IN` msg and sent it to the controller.
   - **PACKET_OUT**: The controller instructing the switch to broadcast the ARP out of specific ports.
   - **FLOW_MOD**: The crucial message. The controller instructs the switch to install a persistent rule in its flow table so subsequent ping packets are forwarded natively in hardware without bothering the controller.

## Expected Outcome
Understanding the anatomy of these messages is a mandatory prerequisite before writing your own controller logic in Python. Pay special attention to how a `FLOW_MOD` matches certain criteria and pushes actions.
