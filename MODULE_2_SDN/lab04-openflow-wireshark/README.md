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
2. Start Mininet with the default topology. The container has a test controller pre-started on port 6653.
   ```bash
   mn --controller=remote
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

2. Scrutinize the packets. The controller in this lab is `ovs-testcontroller`, which operates in a **proactive** fashion: it installs forwarding rules at connection time, before any user traffic is generated. This is different from a *reactive* controller (like the one we will write in Lab 07), which waits for packets to arrive before deciding what to do.

   Locate and inspect the following core OpenFlow messages in the capture. They appear roughly in this order:

   #### Phase 1: Connection Setup
   - **HELLO**: The very first OpenFlow message. Both the switch and the controller exchange `HELLO` to negotiate the protocol version. What version of OpenFlow was negotiated?
   - **FEATURES_REQUEST / FEATURES_REPLY**: The controller asks the switch: *"What can you do? How many ports do you have? What is your Datapath ID?"*. Inspect the `FEATURES_REPLY` — the Datapath ID (DPID) is the switch's unique hardware fingerprint.
   - **SET_CONFIG**: The controller configures how much of each packet should be sent in `PACKET_IN` messages (the `miss_send_len` field).
   - **PORT_STATUS**: The switch informs the controller about the state of its physical ports.

   #### Phase 2: Proactive Rule Installation
   - **FLOW_MOD**: This is the crucial message. The `ovs-testcontroller` installs a rule with `action=NORMAL` immediately upon connection. This tells the switch: *"Handle all traffic using your built-in L2 learning logic — no need to ask me."*
     
     > **Key insight:** Because this rule is installed *before* any ping, the switch will forward the ICMP traffic autonomously. You will **not** see `PACKET_IN`/`PACKET_OUT` messages for the ping traffic itself. The controller has delegated all forwarding decisions to the switch hardware.

   #### Phase 3: Data Plane Traffic (the ping)
   - **PACKET_IN / PACKET_OUT**: You may still see some of these messages in the capture for ARP or initial broadcast traffic that the switch escalates to the controller. Note that these might appear as `(Malformed Packet)` in Wireshark if the OpenFlow version negotiated doesn't match Wireshark's default dissector.

   #### Proactive vs Reactive: A Preview
   | | Proactive (this lab) | Reactive (Lab 07+) |
   |---|---|---|
   | **When are rules installed?** | At connection time | After each unknown packet |
   | **PACKET_IN frequency** | Rare (only edge cases) | Every unknown flow |
   | **Controller load** | Low | High (initially) |
   | **Forwarding latency** | Instant | First packet is slow |

   In Labs 06–09, you will write your own **reactive** controllers in Python (Ryu). There, you will see the full `PACKET_IN → PACKET_OUT → FLOW_MOD` cycle for every new flow.

## Expected Outcome
Understanding the anatomy of these messages is a mandatory prerequisite before writing your own controller logic in Python. Pay special attention to:
- How `HELLO` negotiates the OpenFlow version
- How `FEATURES_REPLY` exposes the switch's identity and capabilities
- How `FLOW_MOD` matches certain criteria and pushes actions — even when installed proactively
