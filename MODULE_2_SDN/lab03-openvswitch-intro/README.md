# Lab 03: Open vSwitch (OVS) and OpenFlow Intro

In this lab, we will break away from Mininet's automated setup to manually explore **Open vSwitch (OVS)**, the default virtual switch platform used by Mininet. You will learn how to manually manage the switch, dump its flow tables, and insert static OpenFlow rules without using an external Controller.

## Setup
Start the container:
```bash
docker compose up -d
docker exec -it asdn_mininet_lab03 /bin/bash
```

## Tasks

### Task 1: Manual Topology Creation
Instead of Mininet doing the heavy lifting, let's create a minimal topology using Mininet's interactive mode, but telling it to use **NO** controller.

1. Start Mininet with a single switch and two hosts, but explicitly specify `controller=none`:
   ```bash
   mn --topo single,2 --controller none
   ```
2. Keep this Mininet CLI open. Because there is no controller, the switch (`s1`) does not know how to forward packets. It has no brain!
3. Try to ping from `h1` to `h2` using the Mininet CLI:
   ```bash
   mininet> h1 ping -c 3 h2
   ```
   **It will fail.** Network is unreachable.

### Task 2: Interacting with OVS
Open a **second terminal window** on your host machine and attach to the running container (`docker exec -it asdn_mininet_lab03 /bin/bash`).

1. List the virtual switches currently running on OVS:
   ```bash
   ovs-vsctl show
   ```
   You should see `s1` listed with its respective interfaces (`s1-eth1`, `s1-eth2`).

2. Dump the current flow table of `s1` using the OpenFlow control tool (`ovs-ofctl`):
   ```bash
   ovs-ofctl dump-flows s1
   ```
   Notice that the table is completely empty (or it only has a single default drop rule). This is exactly why the ping failed in Task 1.

### Task 3: Injecting OpenFlow Rules Manually
We will now act as the "controller" by manually injecting forwarding rules using `ovs-ofctl`.

1. Add a rule to tell `s1` to forward packets arriving on port 1 (from `h1`) out of port 2 (towards `h2`):
   ```bash
   ovs-ofctl add-flow s1 in_port=1,actions=output:2
   ```
2. Add the reverse rule to forward packets arriving on port 2 out of port 1:
   ```bash
   ovs-ofctl add-flow s1 in_port=2,actions=output:1
   ```
3. Dump the flow table again:
   ```bash
   ovs-ofctl dump-flows s1
   ```
   You should now see the two explicit rules you just injected.
4. Go back to your **first terminal window** (where the Mininet CLI is running) and run the ping again:
   ```bash
   mininet> h1 ping -c 3 h2
   ```
   **It should now succeed!**

### Task 4: Explore Flow Statistics
1. In your second terminal, run the flow dump again. 
2. Notice the `n_packets` and `n_bytes` fields next to your rules. They have incremented because your ICMP (ping) traffic matched those exact flows.

Clean up by typing `exit` in the Mininet CLI on the first terminal.
