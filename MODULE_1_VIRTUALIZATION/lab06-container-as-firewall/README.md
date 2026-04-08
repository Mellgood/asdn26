# Lab 06 — Container as Firewall / NAT Gateway

## 🎯 Objective

Expand upon the router built in Lab 05 by deploying `iptables` rules to filter traffic. You will deploy a NAT (Network Address Translation) Gateway that allows an internal network to access the internet, while masquerading their IP addresses. You will also create a DMZ (Demilitarized Zone) and restrict traffic using stateless and stateful firewall rules.

## 📖 Background

### `iptables` Basics

`iptables` is the standard firewall utility for Linux. It inspects and modifies IPv4 packet headers. 

`iptables` uses **Tables** (which categorize rules by purpose) and **Chains** (which categorize rules by when they are applied to the packet lifecycle).

The most relevant chains for a router/firewall are:
- `INPUT`: Packets destined *for* the firewall itself.
- `OUTPUT`: Packets originating *from* the firewall.
- `FORWARD`: Packets passing *through* the firewall (routing).

The most relevant tables are:
- `filter` (default): Used to ACCEPT, DROP, or REJECT packets.
- `nat`: Used to translate IP addresses (SNAT, DNAT, MASQUERADE).

### Stateful Firewalling

A modern firewall doesn't just look at individual packets; it tracks connection states (using `conntrack`). 
- **ESTABLISHED, RELATED**: The packet is part of an existing, approved connection.
- **NEW**: The packet is trying to start a new connection.

It is common to ACCEPT all `ESTABLISHED, RELATED` traffic, and selectively ACCEPT `NEW` traffic based on source/destination/port.

---

## 🔬 Tasks

### Task 1 — Build the Secure Topology

You will build the following topology:

```
      Internet
         │
   (public-net) ───[ Firewall container (eth0) ]
         │                  │
         │ (DMZ/eth1)       │ (Internal/eth2)
         │                  │
   [ Web-Server ]      [ Client-PC ]
```

We will simulate the "Internet" simply by giving our firewall container access to the host's default network (or a bridge attached to outbound). In Compose, the default bridge suffices for this. We will explicitly define the DMZ and Internal networks.

Open `docker-compose.yml`:
1. Define networks `dmz-net` (`172.40.1.0/24`) and `internal-net` (`172.40.2.0/24`). Also use the implicit default compose network (which simulates public internet access).
2. Configure **Client-PC**: Attach to `internal-net`. Add capability `NET_ADMIN`.
3. Configure **Web-Server**: Attach to `dmz-net`. Use the `nginx:alpine` image.
4. Configure **Firewall**: Attach to `internal-net`, `dmz-net`, AND the default network. Add `NET_ADMIN`.

Start the topology:
```bash
docker compose up -d
```

### Task 2 — Implement Routing & NAT

Currently, `client-pc` cannot reach the `web-server` or the internet.

1. First, tell `client-pc` to use the Firewall as its default gateway.
```bash
docker compose exec client-pc ip route del default
docker compose exec client-pc ip route add default via 172.40.2.254
```

2. Tell `web-server` to use the Firewall as its default gateway.
```bash
docker compose exec web-server ip route del default
docker compose exec web-server ip route add default via 172.40.1.254
```

3. Open `firewall-init.sh`. Add commands to do the following:
   - Enable IP forwarding (`sysctl`).
   - Enable NAT (Masquerade) for outgoing traffic from internal and DMZ to the Internet.
     > *Hint: `iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE` (Assuming eth0 is the interface facing the internet).*

Update `docker-compose.yml` to run the `firewall-init.sh` script, similar to Lab 05. Restart your stack. `client-pc` should now be able to ping `8.8.8.8`!

### Task 3 — The Default Drop Policy

A good firewall drops everything by default and only allows explicitly permitted traffic.

1. Modify `firewall-init.sh` to set the default policy for the FORWARD chain to DROP:
   ```bash
   iptables -P FORWARD DROP
   ```

Restart the stack. Try pinging `8.8.8.8` from `client-pc`. It will fail. Try pinging `web-server`. It will fail.

### Task 4 — Allow Traffic based on State

Let's allow internal clients out to the internet, and allow established connections back.

Modify `firewall-init.sh`:
1. **Rule 1**: Allow existing connections to flow freely in all directions.
   ```bash
   iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   ```

2. **Rule 2**: Allow `NEW` connections originating from the `internal-net` (interface `eth2`, if your Compose file assigned them in order. You might need to use `ip addr` to check the exact `ethX` name, or match by subnet `-s 172.40.2.0/24`). Let's use subnets to be interface-agnostic.
   ```bash
   iptables -A FORWARD -s 172.40.2.0/24 -m conntrack --ctstate NEW -j ACCEPT
   ```

Restart `firewall`. Test:
- `client-pc` pinging `8.8.8.8` ➔ ✅ Success
- `client-pc` accessing `web-server` (`curl 172.40.1.10`) ➔ ✅ Success

### Task 5 — Securing the DMZ

The `web-server` should NOT be allowed to initiate connections to `client-pc` (internal). It should only reply to requests.

Because our Rule 1 allows ESTABLISHED traffic, server replies work. Because our Rule 2 *only* allows NEW traffic from `172.40.2.0/24`, the web server cannot initiate connections.

Let's verify this! From the `web-server`, try to ping `client-pc`:
```bash
docker compose exec web-server ping -c 2 172.40.2.10
```
❌ **This should fail.** The DROP policy blocks the `NEW` connection request originating from the DMZ.

### Task 6 — Port Forwarding (DNAT) (Optional Challenge)

Currently everyone on the internet would have to know the `web-server` internal DMZ IP, but NAT hides it. We want external clients to access the `web-server` by hitting the `firewall`'s public IP on port 80.

1. In `firewall-init.sh`, add a DNAT rule:
   ```bash
   # Assuming eth0 is the external interface
   iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 172.40.1.10:80
   ```
2. You also must permit this traffic through the FORWARD chain!
   ```bash
   iptables -A FORWARD -d 172.40.1.10 -p tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT
   ```

Test this by finding the `firewall` container's external IP (`docker inspect ...`) and trying to `curl` it from your host machine!

---

## ✅ Checklist

- [ ] Route traffic out through a NAT MASQUERADE rule
- [ ] Understand and apply a DROP policy
- [ ] Use `conntrack` for a stateful firewall
- [ ] Verify security boundaries between Internal, DMZ, and External

---

## 🧹 Cleanup
```bash
docker compose down
```
