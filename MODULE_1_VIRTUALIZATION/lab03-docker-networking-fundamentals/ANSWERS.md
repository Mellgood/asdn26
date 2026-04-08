# Lab 03 — Docker Networking Fundamentals: Answers

## Task 1 — Default Bridge Network

> **What subnet does the default bridge use? What is the gateway IP?**

The default bridge typically uses `172.17.0.0/16` with gateway `172.17.0.1`. The gateway IP corresponds to the `docker0` bridge interface on the host.

---

## Task 2 — Default Bridge DNS

> **Why doesn't DNS resolution work on the default bridge?**

The default bridge network is a legacy feature. It does **not** run Docker's built-in DNS server for containers. Containers on the default bridge can only communicate by IP address or by using the `--link` flag (deprecated).

User-defined bridges run an embedded DNS server (at `127.0.0.11`) that resolves container names to IP addresses automatically. This is one of the key reasons to **always use user-defined networks** instead of the default bridge.

---

## Task 3 — User-Defined Bridge DNS

> **What DNS server is the container using?**

```bash
$ cat /etc/resolv.conf
nameserver 127.0.0.11
```

Docker's built-in DNS server runs at `127.0.0.11` inside every container on a user-defined network. This server resolves container names and service names.

---

## Task 3 — Network Isolation

> **What provides this isolation?**

Isolation is provided by:
1. **Separate Linux bridges**: Each Docker network creates its own bridge interface. Containers on different bridges are on different L2 segments.
2. **iptables rules**: Docker configures iptables rules to prevent traffic between different bridge networks. Specifically, the `DOCKER-ISOLATION-STAGE-1` and `DOCKER-ISOLATION-STAGE-2` chains drop forwarded packets between bridges.
3. **Different subnets**: Each network uses its own subnet, so containers on different networks don't have routes to each other.

---

## Task 4 — Host Network

> **Compare `ip addr` inside the container with the host.**

They are **identical**. The container sees all host interfaces (eth0, wlan0, docker0, etc.) because it shares the host's network namespace. There is no network isolation — the container operates as if it were a regular process on the host.

---

## Task 5 — None Network

> **When would you want to use `--network none`?**

Use cases for `none` network:
- **Security-sensitive workloads** that should never communicate over the network (e.g., cryptographic key generation, data processing)
- **Batch processing** where you want to ensure no data exfiltration
- **Custom networking** where you want to manually configure networking (add interfaces yourself via `ip link`)
- **Testing** process isolation without network variables

---

## Task 6 — veth Pairs

> **Draw the full network path for a packet from containerA to containerB.**

```
containerA                Host                 containerB
┌──────────┐    ┌──────────────────┐    ┌──────────┐
│          │    │                  │    │          │
│  eth0    │    │    vethAAA       │    │  eth0    │
│  (10.10. │◄──►│       │         │◄──►│  (10.10. │
│   0.2)   │    │       ▼         │    │   0.3)   │
│          │    │   br-XXXXX      │    │          │
│          │    │   (bridge)      │    │          │
│          │    │       ▲         │    │          │
│          │    │       │         │    │          │
│          │    │    vethBBB      │    │          │
└──────────┘    └──────────────────┘    └──────────┘

1. containerA sends packet to eth0 (10.10.0.2)
2. eth0 is one end of a veth pair; the packet appears on vethAAA on the host
3. vethAAA is attached to the bridge (br-XXXXX)
4. The bridge performs MAC learning and forwards to vethBBB
5. vethBBB is the other end of a veth pair; the packet appears on containerB's eth0
6. containerB receives the packet
```

---

## Task 7 — Multi-Network Containers

> **How many `eth` interfaces does the container have?**

Two: `eth0` (connected to `my-network`, e.g., `10.10.0.x`) and `eth1` (connected to `second-network`, e.g., `10.20.0.x`).

> **What routes does the container have? Which network is the default route through?**

```
10.10.0.0/24 dev eth0   # my-network
10.20.0.0/24 dev eth1   # second-network
default via 10.10.0.1 dev eth0  # default route through the first connected network
```

The default route goes through the **first network** the container was connected to.

---

## Task 8 — tcpdump

> **What HTTP method, Host header, and status code were observed?**

- **Method**: `GET /`
- **Host header**: The web server's IP address (e.g., `Host: 10.10.0.3`)
- **Status code**: `200 OK`

The `-A` flag in tcpdump shows the ASCII content of packets, allowing you to see HTTP headers in plain text. This is only possible because HTTP (not HTTPS) traffic is unencrypted.
