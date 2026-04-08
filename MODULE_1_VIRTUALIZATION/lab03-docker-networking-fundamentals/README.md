# Lab 03 — Docker Networking Fundamentals

## 🎯 Objective

Understand Docker's networking model from the inside out. Explore the three main network drivers (bridge, host, none), inspect virtual network interfaces (veth pairs, bridges), and learn how container DNS resolution works. By the end, you'll be ready to design custom network topologies.

## 📖 Background

### How Docker Networking Works

Docker networking relies on **Linux kernel features** — primarily **network namespaces**, **virtual Ethernet pairs (veth)**, and **software bridges**.

#### Network Namespaces

Every container runs in its own **network namespace** — an isolated environment with its own:
- Network interfaces (`eth0`, `lo`)
- Routing table
- iptables rules
- ARP table

```
┌─────────────────────────────────────────────────────────────────┐
│                         HOST                                    │
│                                                                 │
│  ┌──────────────────┐        ┌──────────────────┐               │
│  │  Container A      │        │  Container B      │              │
│  │  (namespace A)    │        │  (namespace B)    │              │
│  │                   │        │                   │              │
│  │  eth0 ──┐        │        │  eth0 ──┐        │              │
│  └─────────┼────────┘        └─────────┼────────┘              │
│            │                           │                        │
│         vethA                       vethB                       │
│            │                           │                        │
│            └───────────┬───────────────┘                        │
│                        │                                        │
│                   docker0 (bridge)                              │
│                        │                                        │
│                      eth0 (host)                                │
│                        │                                        │
└────────────────────────┼────────────────────────────────────────┘
                         │
                    Physical Network
```

#### Virtual Ethernet Pairs (veth)

A **veth pair** is like a virtual network cable with two ends:
- One end is placed inside the container (appears as `eth0`)
- The other end is attached to a bridge on the host (appears as `vethXXXX`)

Anything sent to one end comes out the other.

#### Docker Bridge (`docker0`)

The **default bridge** (`docker0`) is a Linux software bridge that acts as a virtual switch. Containers connected to the same bridge can communicate via Layer 2 (Ethernet frames).

### Docker Network Drivers

| Driver | Description | Use Case |
|--------|------------|----------|
| `bridge` | Containers get their own network namespace, connected via a bridge | Default. Isolated container networking |
| `host` | Container shares the host's network namespace | Performance-critical, no port mapping needed |
| `none` | Container has no network interfaces (except loopback) | Maximum isolation, security |
| `overlay` | Multi-host networking (Docker Swarm) | Covered in Lab 07 |
| `macvlan` | Containers get their own MAC address on the physical network | Advanced, direct LAN access |

---

## 🔬 Prerequisites

Make sure you have built the `net-tools` image from Lab 02:

```bash
docker images net-tools
```

If not, go back to Lab 02, Task 3 and build it.

---

## 🔬 Tasks

### Task 1 — Inspect the Default Bridge Network

Docker creates three default networks on installation:

```bash
docker network ls
```

You should see:

| NAME | DRIVER |
|------|--------|
| `bridge` | `bridge` |
| `host` | `host` |
| `none` | `null` |

Inspect the default bridge:

```bash
docker network inspect bridge
```

> 📝 **Question:** What subnet does the default bridge use? What is the gateway IP? 

Note the `"Containers": {}` field — it's empty because no containers are currently connected.

---

### Task 2 — Containers on the Default Bridge

Run two containers on the default bridge network:

```bash
docker run -d --name containerA net-tools sleep 3600
docker run -d --name containerB net-tools sleep 3600
```

Inspect the bridge network again:

```bash
docker network inspect bridge | jq '.[0].Containers'
```

You should see both containers listed with their IP addresses.

#### Test connectivity by IP

```bash
# Find containerB's IP
CONTAINER_B_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerB)
echo "Container B IP: $CONTAINER_B_IP"

# Ping from containerA to containerB
docker exec containerA ping -c 3 $CONTAINER_B_IP
```

✅ This should work — containers on the same bridge can reach each other by IP.

#### Test connectivity by name (DNS)

```bash
docker exec containerA ping -c 3 containerB
```

❌ **This will fail!** The default bridge does **not** provide automatic DNS resolution between containers. You can only reach containers by IP address.

> 📝 **Question:** Why doesn't DNS resolution work on the default bridge? This is a key difference from user-defined bridges (next task).

#### Clean up

```bash
docker stop containerA containerB && docker rm containerA containerB
```

---

### Task 3 — User-Defined Bridge: DNS and Isolation

Create a custom bridge network:

```bash
docker network create --driver bridge --subnet 10.10.0.0/24 --gateway 10.10.0.1 my-network
```

Inspect it:

```bash
docker network inspect my-network
```

Run two containers on this network:

```bash
docker run -d --name hostA --network my-network net-tools sleep 3600
docker run -d --name hostB --network my-network net-tools sleep 3600
```

#### Test DNS resolution

```bash
docker exec hostA ping -c 3 hostB
```

✅ **This works!** User-defined bridges provide **automatic DNS resolution** using container names.

```bash
# Verify DNS is working
docker exec hostA dig hostB
docker exec hostA nslookup hostB
```

> 📝 **Question:** What DNS server is the container using? (Hint: check `cat /etc/resolv.conf` inside the container)

#### Test isolation from default bridge

Run a container on the default bridge:

```bash
docker run -d --name outsider net-tools sleep 3600
```

Try to reach `hostA` from `outsider`:

```bash
HOST_A_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' hostA)
docker exec outsider ping -c 3 $HOST_A_IP
```

❌ **This should fail!** Containers on different networks are isolated from each other.

> 📝 **Question:** What provides this isolation? Think about Linux bridges and routing rules.

#### Clean up

```bash
docker stop hostA hostB outsider && docker rm hostA hostB outsider
```

---

### Task 4 — Host Network Mode

Run a container using the host network:

```bash
docker run -it --rm --network host net-tools bash
```

Inside the container:

```bash
ip addr
ip route
hostname
cat /etc/hostname
```

> 📝 **Question:** Compare the output of `ip addr` inside the container with the host. What do you notice? How many interfaces does the container see?

The container sees **all** of the host's network interfaces. There is **no isolation** — the container shares the host's entire network stack.

**Port mapping is not needed (and not supported) in host mode** — the container binds directly to host ports.

Type `exit` to leave.

---

### Task 5 — None Network Mode

Run a container with no network:

```bash
docker run -it --rm --network none net-tools bash
```

Inside the container:

```bash
ip addr
ping 8.8.8.8
```

You should see **only** the loopback interface (`lo`). The container cannot reach anything — complete network isolation.

> 📝 **Question:** When would you want to use `--network none`?  
> 💡 Think about security-sensitive workloads that should never communicate over the network.

Type `exit` to leave.

---

### Task 6 — Deep Dive: Inspecting veth Pairs and Bridges

**⚠️ Note:** This task works best on a **Linux host** where Docker runs natively. On macOS and Windows, Docker runs inside a lightweight VM, so host-level inspection of network interfaces requires entering that VM.

#### On Linux

Run a container:

```bash
docker run -d --name veth-test --network my-network net-tools sleep 3600
```

##### Step 1: Find the veth pair inside the container

```bash
docker exec veth-test ip link show eth0
```

Note the interface index — you'll see something like: `42: eth0@if43` — where `43` is the peer interface index on the host.

##### Step 2: Find the corresponding veth on the host

```bash
ip link show | grep -A1 "^43:"
```

You should see a `vethXXXXXX` interface that is attached to a bridge.

##### Step 3: Find the bridge

```bash
bridge link show
# or
ip link show type bridge
```

You should see a bridge named something like `br-XXXXXXXXXXXX` (corresponding to `my-network`).

##### Step 4: Visualize the full path

```
containerA:eth0 ↔ vethXXX ↔ bridge (br-XXX) ↔ vethYYY ↔ containerB:eth0
```

#### On macOS / Windows (Docker Desktop)

Since Docker Desktop runs in a VM, you can use this workaround to inspect the host-level networking:

```bash
# Enter the Docker Desktop VM
docker run -it --rm --privileged --pid=host alpine nsenter -t 1 -m -u -n -i sh

# Now you can run:
ip link show
bridge link show
iptables -t nat -L
```

> 📝 **Question:** Draw the full network path for a packet going from `containerA` to `containerB` on the same bridge. Include all interfaces and the bridge.

---

### Task 7 — Multi-Network Containers

A single container can be connected to **multiple networks** simultaneously:

```bash
# Create a second network
docker network create --driver bridge --subnet 10.20.0.0/24 --gateway 10.20.0.1 second-network

# Run a container on the first network
docker run -d --name multi-homed --network my-network net-tools sleep 3600

# Connect it to the second network too
docker network connect second-network multi-homed
```

Inspect the container's network interfaces:

```bash
docker exec multi-homed ip addr
```

> 📝 **Question:** How many `eth` interfaces does the container have? What IP addresses were assigned?

```bash
docker exec multi-homed ip route
```

> 📝 **Question:** What routes does the container have? Which network is the default route through?

#### Test: Container as a bridge between networks

Run a container on only `second-network`:

```bash
docker run -d --name isolated-host --network second-network net-tools sleep 3600
```

From `multi-homed`, can you reach both networks?

```bash
# Reach a container on my-network
docker exec multi-homed ping -c 2 hostA 2>/dev/null || echo "No hostA running"

# Reach the isolated host on second-network
ISOLATED_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' isolated-host)
docker exec multi-homed ping -c 2 $ISOLATED_IP
```

> 💡 This multi-homed pattern is the foundation for Lab 05, where you'll configure a container as a **router** between two isolated networks.

---

### Task 8 — Capture Traffic with tcpdump

Let's observe actual network traffic between containers using `tcpdump`.

#### Setup

```bash
# Make sure we have containers running (reuse or create new ones)
docker run -d --name sniffer --network my-network net-tools sleep 3600
docker run -d --name webserver --network my-network -e "HOSTNAME=webserver" nginx
```

#### Capture ICMP (ping) traffic

In one terminal, start `tcpdump` on the sniffer:

```bash
docker exec sniffer tcpdump -i eth0 icmp -n
```

In another terminal, ping the webserver from the sniffer:

```bash
WEBSERVER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' webserver)
docker exec sniffer ping -c 3 $WEBSERVER_IP
```

You should see the ICMP echo request and reply packets in the `tcpdump` output.

#### Capture HTTP traffic

In one terminal:

```bash
docker exec sniffer tcpdump -i eth0 port 80 -A -n
```

In another terminal:

```bash
WEBSERVER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' webserver)
docker exec sniffer curl http://$WEBSERVER_IP
```

The `-A` flag shows the packet content in ASCII — you should see the HTTP request and response headers!

> 📝 **Question:** In the captured HTTP traffic, what HTTP method was used? What was the `Host` header? What was the response status code?

---

## 🧹 Cleanup

```bash
# Remove all containers
docker stop $(docker ps -q) 2>/dev/null
docker container prune -f

# Remove custom networks
docker network rm my-network second-network 2>/dev/null

# Verify
docker network ls
docker ps -a
```

---

## ✅ Checklist

Before moving to the next lab, make sure you can:

- [ ] Explain the difference between bridge, host, and none network drivers
- [ ] Create custom bridge networks with specific subnets
- [ ] Explain why user-defined bridges support DNS but the default bridge doesn't
- [ ] Inspect veth pairs and understand the container ↔ bridge ↔ container path
- [ ] Connect a container to multiple networks
- [ ] Use `tcpdump` to capture and analyze container traffic
- [ ] Explain network isolation between different Docker networks

---

## 🗺️ Concepts Map

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Networking                         │
│                                                             │
│  ┌───────────┐    ┌──────────┐    ┌───────────────────┐    │
│  │  bridge    │    │  host    │    │  none             │    │
│  │           │    │          │    │                   │    │
│  │ - Default │    │ - Shares │    │ - Loopback only  │    │
│  │ - Custom  │    │   host   │    │ - No network     │    │
│  │ - DNS on  │    │   stack  │    │ - Max isolation  │    │
│  │   custom  │    │ - No     │    │                   │    │
│  │ - Isolated│    │   isolation│   │                   │    │
│  └───────────┘    └──────────┘    └───────────────────┘    │
│                                                             │
│  Key mechanisms: namespaces, veth pairs, bridges, iptables  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Further Reading

- [Docker Networking Documentation](https://docs.docker.com/network/)
- [Linux Network Namespaces](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)
- [Bridge Networking Deep Dive](https://docs.docker.com/network/bridge/)
- [tcpdump Tutorial](https://danielmiessler.com/study/tcpdump/)
