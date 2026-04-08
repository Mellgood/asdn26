# Lab 08 — Multi-Segment Network Topology (Capstone)

## 🎯 Objective

Synthesize all the skills you've learned in Module 1 to build a realistic multi-segment enterprise topology. You will configure everything using `docker-compose.yml` and custom startup scripts.

## 📖 Background

You've been tasked with designing the virtual network infrastructure for **ASDN Corp**. They require a secure design with isolated segments:
1. An **Internal Network** where employee workstations and internal services (DNS) reside.
2. A **DMZ (Demilitarized Zone)** where public-facing services (Web Server) reside.
3. An **Edge Firewall** that protects the network and provides internet access via NAT.
4. An **Internal Core Router** that connects the internal network to the DMZ.

### The Target Topology

```
                    ┌──────────┐
                    │ INTERNET │ (Docker default bridge network)
                    └────┬─────┘
                         │ eth0 (DHCP IP)
                    ┌────┴─────┐
                    │ FIREWALL │ (NAT, iptables rules)
                    └────┬─────┘
                         │ eth1 (172.20.1.253)
                         │
     DMZ-NET (172.20.1.0/24) ────┬──────────────┐
                                 │              │
                           ┌─────┴────┐    ┌────┴─────┐
    eth0 (172.20.1.10)     │ WEB-SRV  │    │  ROUTER  │ eth0 (172.20.1.254)
                           └──────────┘    └────┬─────┘
                                                │ eth1 (172.20.2.254)
                                                │
INTERNAL-NET (172.20.2.0/24) ───┬───────────────┼───────────────┐
                                │               │               │
                         ┌──────┴───┐     ┌─────┴────┐     ┌────┴─────┐
     (172.20.2.101)      │ CLIENT-1 │     │ CLIENT-2 │     │ DNS-SRV  │ (172.20.2.10)
                         └──────────┘     └──────────┘     └──────────┘
```

---

## 🔬 Tasks

### Task 1 — Build the Skeleton 

1. Open `docker-compose.yml`. You must use defining blocks to build the entire topology.
2. Use the `net-tools` image for the Router, Firewall, and Clients. Use `nginx:alpine` for the Web-SRV. Use `coredns/coredns` or `ubuntu` for DNS (we'll just use `net-tools` here and run a fake DNS or just use it as a ping target for simplicity). Let's use `net-tools` for DNS-SRV, it responds to ping!
3. Ensure the Firewall, Router, and Clients all have `NET_ADMIN` privileges.
4. Assign IP addresses exactly according to the topology diagram.

### Task 2 — Implement Core Routing

To make communication possible, routing tables must be updated across the infrastructure. We've provided empty script files for you. Add `sysctl` IP forwarding and `ip route` commands to them.

1. **Clients (1 & 2) and DNS-SRV**: Their default gateway must be the **Router** (`172.20.2.254`).
2. **WEB-SRV**: Its default gateway must be the **Firewall** (`172.20.1.253`), allowing it internet access. But we *also* need it to talk to the internal network. Add a specific static route: `172.20.2.0/24 via 172.20.1.254`.
3. **Router**: Must have IP forwarding enabled. Its default gateway must be the **Firewall** (`172.20.1.253`). This handles traffic from the internal net to the internet.
4. **Firewall**: Must have IP forwarding enabled. It needs a return static route to the internal network: `172.20.2.0/24 via 172.20.1.254`.

### Task 3 — Configure the Firewall NAT

In `firewall-init.sh`, configure `iptables` to MASQUERADE outgoing traffic on the interface connected to the internet. (Note: In Compose, the firewall will likely be connected to 3 networks total or 2 networks + default. Find out which one is the external interface using `ip -4 route ls | grep default`).

### Task 4 — Test End-to-End Connectivity

Bring up the stack and run these tests:

1. **Internal to DMZ**:
   ```bash
   docker compose exec client-1 ping -c 2 172.20.1.10
   ```
2. **Internal to Internet**:
   ```bash
   docker compose exec client-1 ping -c 2 8.8.8.8
   ```
3. **Multi-hop Traceroute**:
   ```bash
   docker compose exec client-1 traceroute 8.8.8.8
   ```
   You should clearly see it pass through `172.20.2.254` (Router), then `172.20.1.253` (Firewall) before reaching the ISP!

### Task 5 — Securing the Environment (The Final Challenge)

Right now, there are no firewall rules, only NAT. 
Add `iptables` rules on the Firewall (`firewall-init.sh`) so that:
1. `ESTABLISHED, RELATED` connections are permitted across the board.
2. The `internal-net` is allowed to access the Internet (`NEW` state).
3. The `internal-net` is allowed to access the DMZ.
4. The `dmz-net` is **DENIED** from initiating connections into the `internal-net`.
5. Apply a default `DROP` policy on the FORWARD chain.

Try initiating a `ping` from `web-srv` to `client-1`. It should fail, proving your network architecture is both routed and secure!

---

## 🏆 Congratulations!

If you completed this capstone, you now deeply understand container virtual networking, Linux routing, subnets, and stateful firewalls.

## 🧹 Cleanup
```bash
docker compose down
```
