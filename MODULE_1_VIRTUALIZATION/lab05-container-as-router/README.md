# Lab 05 — Container as a Router

## 🎯 Objective

Transform a Docker container into a fully functional router capable of forwarding packets between two isolated networks. This lab bridges the gap between basic container usage and advanced network engineering.

## 📖 Background

By default, Linux kernels are configured as **hosts** — they drop packets that are not addressed to them. To make a Linux machine (or a container) act as a **router**, two criteria must be met:

1. **Multi-homed:** It must be connected to at least two networks.
2. **IP Forwarding enabled:** The kernel must be told to accept packets for other destinations and forward them according to its routing table.

### IP Forwarding

In Linux, forwarding is controlled by the `sysctl` parameter `net.ipv4.ip_forward`.
- `0`: disabled (default)
- `1`: enabled

### Architecture

You will build the following topology:

```
        Host-A                            Host-B
    (10.5.1.10)                        (10.5.2.10)
        │                                  │
    net-alpha                          net-beta
  (10.5.1.0/24)                      (10.5.2.0/24)
        │                                  │
        └──────────────┐    ┌──────────────┘
                       │    │
                  eth0 │    │ eth1
                (10.5.1.1) (10.5.2.1)
                   ┌───┴────┴───┐
                   │   Router   │
                   └────────────┘
```

Both `Host-A` and `Host-B` are completely isolated. The `Router` has a leg in both networks.

---

## 🔬 Tasks

### Task 1 — Build the Topology

We will use Docker Compose to define the topology.

Open `docker-compose.yml` and complete the `TODO` sections:
1. Define the networks: `net-alpha` (`10.5.1.0/24`) and `net-beta` (`10.5.2.0/24`).
2. Add the `host-a` container. Use the `net-tools` image from Lab 02. Attach it to `net-alpha` with IP `10.5.1.10`.
3. Add the `host-b` container. Use the `net-tools` image. Attach it to `net-beta` with IP `10.5.2.10`.
4. Add the `router` container. Use the `net-tools` image. Attach it to BOTH networks, with IP `10.5.1.1` on `net-alpha` and `10.5.2.1` on `net-beta`.

Start the topology:
```bash
docker compose up -d
```

### Task 2 — Verify Initial Reachability (or Lack Thereof)

Let's test from Host-A. Enter its shell:

```bash
docker compose exec host-a bash
```

Inside `host-a`, try these commands:
```bash
ping -c 2 10.5.1.1   # Ping the router's interface on net-alpha. Should work.
ping -c 2 10.5.2.10  # Ping Host-B. Should FAIL.
exit
```

> 📝 **Question:** Why does the ping to Host-B fail? (Hint: There are two distinct issues right now, one on the host, one on the router.)

### Task 3 — Add Routes to the Hosts

`Host-A` knows about the `10.5.1.0/24` network. However, it doesn't know how to reach `10.5.2.0/24`. It needs a route.

By default, Docker containers get a default route pointing to the docker bridge gateway (e.g. `10.5.1.254`). We need to tell `Host-A` to use the `Router` container (`10.5.1.1`) to reach `net-beta`.

```bash
# Add route to Host-A
docker compose exec -u root host-a ip route add 10.5.2.0/24 via 10.5.1.1

# Add route to Host-B (to reach net-alpha via the router)
docker compose exec -u root host-b ip route add 10.5.1.0/24 via 10.5.2.1
```

Now try the ping from `host-a` again:
```bash
docker compose exec host-a ping -c 2 10.5.2.10
```

❌ **It still fails.**

Wait, the routing table is correct! Why does it fail? Because the router drops the forwarded packet.

### Task 4 — Enable IP Forwarding on the Router

The container `router` is receiving the packet destined for `10.5.2.10`, but its kernel drops it because `net.ipv4.ip_forward` is `0`.

Check the current value:
```bash
docker compose exec router sysctl net.ipv4.ip_forward
```

Enable it:
```bash
docker compose exec -u root router sysctl -w net.ipv4.ip_forward=1
```

> ⚠️ Note: For this to work, the `router` container needs a special capability in the docker-compose file: `cap_add: - NET_ADMIN`. Ensure this is present in your completed Compose file.

Now test from `host-a` again:
```bash
docker compose exec host-a ping -c 2 10.5.2.10
```

✅ **Success!** You have built a router.

### Task 5 — Automate the Configuration

Typing `sysctl` and `ip route` every time the containers restart is tedious.

In this directory, there is a `router-init.sh` script.

1. Modify `router-init.sh` to enable IP forwarding automatically.
2. Update the `docker-compose.yml` to mount this script into the router container and run it at startup. Look at the `command` field under `router` for a hint.
3. To add routes on `host-a` and `host-b` automatically, you can pass the `ip route add` command to their `command` definition in the Compose file. Note that a container exits when its command finishes, so you must append `&& tail -f /dev/null` to keep them running!

Example for host-a:
```yaml
command: bash -c "ip route add 10.5.2.0/24 via 10.5.1.1 && tail -f /dev/null"
```

Tear down and restart your stack to verify the automation works.

```bash
docker compose down
docker compose up -d
docker compose exec host-a ping -c 2 10.5.2.10
```

### Task 6 — Verify the Path with Traceroute

To prove traffic is actually going through the router:

```bash
docker compose exec host-a traceroute 10.5.2.10
```

You should see two hops:
1. `10.5.1.1` (Router)
2. `10.5.2.10` (Host-B)

---

## ✅ Checklist

- [ ] Complete the topology in `docker-compose.yml`
- [ ] Understand why manual routing table entries are needed on the hosts
- [ ] Understand `net.ipv4.ip_forward` and `NET_ADMIN` capability
- [ ] Successfully ping between the isolated hosts
- [ ] Follow the packet path via traceroute

---

## 🧹 Cleanup
```bash
docker compose down
```
