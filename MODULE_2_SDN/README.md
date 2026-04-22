# Module 2: SDN, Controllers and Kathará

Welcome to **Module 2** of the ASDN course! In this section, we will transition from basic virtualization to complex network emulation using the **Software Defined Networking (SDN)** paradigm.

## 🎯 Module Objectives

* Understand the inner workings of protocols such as **OpenFlow**
* Utilize complex network emulators like **Mininet** and **Kathará**
* Programmatically design topologies using Python
* Explore the development of both educational **SDN Controllers** (Ryu, POX) and enterprise-grade ones (ONOS, OpenDaylight)
* Integrate SDN concepts with traditional routing (OSPF, BGP)

## 🐳 Environment Setup

To ensure consistency, the majority of the labs will utilize Docker.
Inside the `docker/` folder, you will find the base `Dockerfile.sdn` which includes all the necessary tools:
* Mininet, Open vSwitch
* Ryu Controller
* tcpdump, tshark, iperf, ping

Each lab will feature its own `docker-compose.yml` file or specific startup instructions.

---

## 🐍 Python API Reference

We keep track of the Python and Mininet syntax introduced during the labs so you can easily reference them later.

| Command | Description | Introduced In |
|---------|-------------|---------------|
| `self.addSwitch('name')` | Instantiates a virtual switch. | [Lab 02](lab02-mininet-python-api/) |
| `self.addHost('name')` | Instantiates a virtual host. | [Lab 02](lab02-mininet-python-api/) |
| `self.addLink(n1, n2, **params)` | Creates a physical link between two nodes. | [Lab 02](lab02-mininet-python-api/) |
| `Mininet(topo, controller, link)` | The main class initializing the network. | [Lab 02](lab02-mininet-python-api/) |
| `net.start()`, `net.stop()` | Starts and cleanly stops the network. | [Lab 02](lab02-mininet-python-api/) |
| `CLI(net)` | Opens the interactive Mininet CLI. | [Lab 02](lab02-mininet-python-api/) |
| `controller=None` | Starts Mininet without an automated local controller. | [Lab 05](lab05-openflow-manual-routing/) |
| `parser.OFPActionOutput(port)` | Ryu API to dictate a physical forwarding action. | [Lab 06](lab06-hub-controller-ryu/) |
| `parser.OFPPacketOut(...)` | Constructs a robust OpenFlow PACKET_OUT message. | [Lab 06](lab06-hub-controller-ryu/) |
| `datapath.send_msg(msg)` | The generic Ryu method to send ANY payload to the Switch. | [Lab 06](lab06-hub-controller-ryu/) |
| `parser.OFPMatch(...)` | Creates pattern match conditions (e.g., `in_port`, `eth_dst`, `ipv4_src`). | [Lab 07](lab07-learning-switch-ryu/) |
| `parser.OFPFlowMod(...)` | Constructs a permanent rule to be injected into the hardware. | [Lab 07](lab07-learning-switch-ryu/) |
| `parser.OFPActionSetField(...)` | Modifies packet headers directly hardware-side (e.g., `ipv4_dst`). | [Lab 09](lab09-sdn-loadbalancer-ryu/) |
| `requests.post(ONOS_API, ...)` | Interfaces elegantly with REST Northbound APIs using standard HTTP verbs. | [Lab 11](lab11-onos-rest-intents/) |
| `requests.get(ODL_API, ...)` | Fetches operational data stores (like topologies). | [Lab 12](lab12-opendaylight-basics/) |

---

## 🐢 Kathará Reference

| Syntax / Environment Command | Description | Introduced In |
|------------------------------|-------------|---------------|
| `node[port]="domain"` | Declares a topological cross-connect in `lab.conf`. | [Lab 13](lab13-kathara-routing-basics/) |
| `ip addr add <ip> dev <iface>` | Native Linux command to firmly assign an IPv4 address to an interface in `.startup` files. | [Lab 13](lab13-kathara-routing-basics/) |
| `ip route add <net> via <gw>` | Injects a static route directly into the Linux kernel OS table. | [Lab 13](lab13-kathara-routing-basics/) |
| `router ospf` / `network <net> area <id>`| FRRouting syntax to activate OSPF in `.conf` files. | [Lab 14](lab14-kathara-ospf-wireshark/) |
| `tcpdump -w /shared/...`| Captures packets in a Kathará shared folder accessible from the Host. | [Lab 14](lab14-kathara-ospf-wireshark/) |
| `router bgp <as>` / `neighbor <ip> remote-as <as>`| FRRouting syntax to establish eBGP adjacencies. | [Lab 15](lab15-kathara-bgp-peering/) |
| `node[image]="kathara/sdn"`| Overrides the default Kathará container to use one equipped with Open vSwitch. | [Lab 16](lab16-kathara-sdn-integration/) |

---

## 🌉 Open vSwitch Reference

| Syntax / Environment Command | Description | Introduced In |
|------------------------------|-------------|---------------|
| `ovs-vsctl add-br <name>` | Creates a virtual logical bridge (switch). | [Lab 03](lab03-openvswitch-intro/) |
| `ovs-vsctl add-port <br> <port>` | Hooks a physical or virtual interface to the switch natively. | [Lab 03](lab03-openvswitch-intro/) |
| `ovs-ofctl dump-flows <br>` | Actively sniffs the live OpenFlow rules currently written in hardware. | [Lab 03](lab03-openvswitch-intro/) |
| `/etc/init.d/openvswitch-switch start` | Safely initializes the Open vSwitch daemon. | [Lab 16](lab16-kathara-sdn-integration/) |
| `ovs-vsctl set-controller <br> tcp:<ip>:<port>` | Arbitrarily forces an OVS switch to be managed by a remote controller. | [Lab 16](lab16-kathara-sdn-integration/) |

---

## 📚 Labs Directory

The module is thoughtfully divided into logical sections. Please work through the exercises sequentially, as concepts accumulate over time.

### Section 1: Introductory OpenFlow & Mininet
* [Lab 01: Mininet Basics](lab01-mininet-basics/)
* [Lab 02: Mininet Python API](lab02-mininet-python-api/)
* [Lab 03: Open vSwitch Intro](lab03-openvswitch-intro/)
* [Lab 04: OpenFlow Wireshark](lab04-openflow-wireshark/)
* [Lab 05: Manual OpenFlow Routing](lab05-openflow-manual-routing/)

### Section 2: SDN Python Controllers (Ryu)
* [Lab 06: Ryu Hub Controller](lab06-hub-controller-ryu/)
* [Lab 07: Ryu L2 Learning Switch](lab07-learning-switch-ryu/)
* [Lab 08: Ryu Firewall](lab08-sdn-firewall-ryu/)
* [Lab 09: Ryu Load Balancer](lab09-sdn-loadbalancer-ryu/)

### Section 3: Enterprise SDN (ONOS & OpenDaylight)
* [Lab 10: ONOS Introduction & GUI](lab10-onos-intro-and-gui/)
* [Lab 11: ONOS REST API & Intents](lab11-onos-rest-intents/)
* [Lab 12: OpenDaylight Basics](lab12-opendaylight-basics/)

### Section 4: Advanced Network Emulation (Kathará)
* [Lab 13: Kathará Routing Basics](lab13-kathara-routing-basics/)
* [Lab 14: Dynamic Routing with OSPF](lab14-kathara-ospf-wireshark/)
* [Lab 15: eBGP Peering (Exterior Gateway Protocol)](lab15-kathara-bgp-peering/)
* [Lab 16: SDN Integration in Kathará](lab16-kathara-sdn-integration/)
