# Lab 17: Multi-Switch SDN Fabric in Kathará

In Lab 16, we used a single SDN switch inside Kathará. But real SDN deployments use **many switches**, all managed by a **single centralized controller**. This is where the true power of SDN shines: one brain orchestrating the entire network.

In this lab, we will build a chain of 3 OpenFlow switches inside Kathará. A single Ryu Learning Switch controller (from Lab 07) will manage all of them simultaneously. Traffic from `h1` to `h2` must traverse **all three switches**, and the controller must learn MAC addresses on each one independently.

## Topology

```mermaid
graph LR
    subgraph MGMT["Management Network (172.16.0.0/24)"]
        ctrl{{"controller: 172.16.0.1"}}
    end
    h1[h1: 10.0.0.1]
    s1((s1))
    s2((s2))
    s3((s3))
    h2[h2: 10.0.0.2]

    ctrl -.-|MGMT| s1
    ctrl -.-|MGMT| s2
    ctrl -.-|MGMT| s3
    h1 ---|A| s1
    s1 ---|B| s2
    s2 ---|C| s3
    s3 ---|D| h2
```

Traffic path: `h1 → s1 → s2 → s3 → h2`

## Key Concepts
- **Centralized Control**: A single controller can manage dozens of switches. Each switch independently sends `PACKET_IN` messages and receives `FLOW_MOD` rules.
- **Multi-hop L2 Forwarding**: The Learning Switch floods unknown MACs. Since switches are chained, the flood propagates through the entire fabric until the destination is found.
- **Per-switch Flow Tables**: Each switch has its own independent flow table. After the first ping, `ovs-ofctl dump-flows` will show different rules on each switch (because MAC→port mappings differ per switch).
- **Management Network**: The controller communicates with switches over a dedicated out-of-band network (172.16.0.0/24), separate from the data plane.

## Setup (one-time)
Build the controller image (only needed once, shared across all labs):

🖥️ **Host terminal**:
```bash
docker build -t asdn/sdn -f ../docker/Dockerfile.sdn ../docker/
```

## Tasks

### Task 1: Complete the Topology (`lab.conf`)
1. Open `lab.conf`. We provided the controller node (pre-configured) and the full configuration for `s1` (SDN image + connections to domains A, B, and MGMT).
2. Complete the `TODO`s to define `s2` and `s3` with their respective domain connections, the `kathara/sdn` image override, **and the MGMT domain**.
3. Connect `h1` to domain A and `h2` to domain D.

### Task 2: Configure the Switches (`.startup` files)
1. Open `s1.startup`. It contains the complete OVS setup: starting the daemon, creating the bridge, adding data ports, management interface, and connecting to the controller.
2. Open `s2.startup` and `s3.startup`. Complete the `TODO`s following the exact same pattern as `s1.startup`. Each switch must:
   - Start the OVS daemon
   - Create a bridge with the **same name as the node** (e.g., `s2` for the s2 node)
   - Add its data interfaces (`eth0`, `eth1`) to the bridge — do **NOT** add `eth2` (that's the management interface)

> **Note:** The management interface (`eth2`) and controller connection are pre-configured in each `.startup` file. You only need to fill in the OVS bridge and port setup.

### Task 3: Start and Verify

🖥️ **Host terminal** (from this lab's directory):
```bash
kathara lstart
```

The controller starts automatically. Wait ~5 seconds, then:

1. 📦 From **h1's Kathara terminal**, ping h2:
   ```bash
   ping 10.0.0.2
   ```
2. 📦 Watch the **controller's Kathara terminal** — you should see `PACKET_IN` events from **three different datapaths** (s1, s2, s3). The controller learns MACs on each switch independently.
3. 📦 From any **switch terminal** (e.g., s2), inspect the installed flow rules:
   ```bash
   ovs-ofctl dump-flows s2
   ```
   You should see rules with specific `dl_dst` (destination MAC) entries and corresponding `output:N` actions — proving that the Learning Switch has programmed hardware-level rules on each switch.

### Task 4 (Advanced): Observe the Flood Chain
1. 📦 Open **h2's terminal** and start a packet capture:
   ```bash
   tcpdump -i eth0
   ```
2. 📦 From **h1**, ping a **non-existent** IP (e.g., `ping 10.0.0.99`). Since no host has that IP, the ARP request will flood through the entire s1→s2→s3 chain. You should see the ARP request arriving on h2's capture, proving that FLOOD traverses the whole fabric.
