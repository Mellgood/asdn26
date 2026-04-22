# Solutions for Lab 04

There are no coding scripts required. However, when inspecting the `openflow_capture.pcap` file in Wireshark, you should observe the following chronological sequence of OpenFlow packets (often encapsulated over TCP/IPv4):

1. **Protocol TCP 3-way Handshake** (`SYN`, `SYN-ACK`, `ACK`) on port `6653` (or `6633`).
2. **OFPT_HELLO** (Type 0): Both entities exchange their Highest Supported OpenFlow versions. OVS typically advertises OF 1.5, while Mininet's reference controller negotiates OF 1.0 or OF 1.3.
3. **OFPT_FEATURES_REQUEST** (Type 5): Controller asks the switch "Who are you?".
4. **OFPT_FEATURES_REPLY** (Type 6): Switch responds with its DPID (datapath identifier) and structural properties.
5. **OFPT_PACKET_IN** (Type 10): If you expand this packet in Wireshark, you'll see it contains the encapsulated Ethernet frame (often an ARP Request from `h1` looking for `h2`'s IP).
6. **OFPT_PACKET_OUT** (Type 13): Controller orders the switch to flood/broadcast the encapsulated ARP payload out of `FLOOD` or `ALL` ports.
7. **OFPT_FLOW_MOD** (Type 14): After the ARP is resolved and ICMP is sent, the controller injects a flow rule. The `FLOW_MOD` message will contain the `Match` fields (e.g., `in_port=1`, `eth_dst=12:34:56...`) and `Actions` (e.g., `output:2`). Once injected, the switch handles the traffic at line-rate.
