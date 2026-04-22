# Lab 01: Mininet Basics

In this lab, you will familiarize yourself with **Mininet**, a powerful network emulator. You will learn how to create different types of predefined topologies and how to test network connectivity and bandwidth using standard tools such as `ping` and `iperf`.

## ⚙️ Setup

Start the Mininet container using Docker Compose. Since Mininet needs to manipulate network namespaces and interfaces on the host kernel, we run it in `privileged` mode.

```bash
docker compose up -d
docker exec -it asdn_mininet_lab01 /bin/bash
```

## 📝 Tasks

### Task 1: The Default Topology
Once inside the container, start Mininet with the default topology (a single switch with two hosts) by simply running:

```bash
mn
```

You are now in the Mininet CLI (`mininet>`).
1. Verify what nodes are present using the `nodes` command.
2. Check the links between nodes using `net`.
3. Verify connectivity between the two hosts by running `h1 ping -c 3 h2` in the Mininet CLI.
4. Exit Mininet by typing `exit` or pressing `Ctrl+D`. Ensure you run `mn -c` to clean up residual configurations.

### Task 2: Linear and Tree Topologies
Mininet supports several parameterized topologies out of the box.

1. Create a **linear** topology with 4 switches (each with one host attached):
   ```bash
   mn --topo linear,4
   ```
   Check the connections using the `net` command and run a generic `pingall` to verify that all hosts can reach each other. Clean up after exiting.

2. Create a **tree** topology with depth 2 and fanout 2:
   ```bash
   mn --topo tree,depth=2,fanout=2
   ```
   How many switches are created? How many hosts? Test the connectivity using `pingall`. Clean up.

### Task 3: Bandwidth Testing with `iperf`
Mininet allows you to easily simulate bandwidth tests between virtual hosts.

1. Start the default topology again (`mn`).
2. Run `iperf` directly from the Mininet CLI between h1 and h2:
   ```bash
   iperf h1 h2
   ```
3. By default, links have no limits. Try starting Mininet with custom link constraints (e.g., 10 Mbps bandwidth and 10ms delay) using the `TCLink` class:
   ```bash
   mn --link tc,bw=10,delay=10ms
   ```
4. Run `iperf` again. You should now see the bandwidth capped at around 10 Mbps. Test the ping latency as well (`h1 ping -c 3 h2`); you should see a ~20ms RTT.

Clean up the environment (`mn -c`) once you are done.
