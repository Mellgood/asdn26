# Lab 07 — VLAN and Overlay Networks

## 🎯 Objective

Understand how to implement Virtual LANs (VLANs) using 802.1Q and how to create VXLAN overlay tunnels inside Docker containers. This introduces fundamental Software Defined Networking (SDN) concepts.

## 📖 Background

### VLANs (802.1Q)
A VLAN allows you to logically segment a single physical (or virtual L2) network into multiple isolated broadcast domains. It does this by inserting a 4-byte VLAN tag into the Ethernet frame header (802.1Q).
In Linux, you can create a "sub-interface" (e.g., `eth0.10` for VLAN 10) that tags outgoing traffic and strips tags from incoming traffic matching that ID.

### Overlays & VXLAN
An overlay network is a virtual network built on top of an underlying physical network (the "underlay").
**VXLAN (Virtual eXtensible LAN)** is an encapsulation protocol that wraps Layer 2 Ethernet frames inside Layer 4 UDP packets. It allows L2 networks to span across L3 boundaries (routers/internet).

---

## 🔬 Tasks

### Task 1 — Prepare the Topology

We will start with a single shared Docker bridge network (`shared-net`). Both containers will be on this network.

1. Open `docker-compose.yml` and define the network `shared-net` (`172.50.0.0/24`).
2. Define two containers: `host-a` (`172.50.0.10`) and `host-b` (`172.50.0.20`), using your `net-tools` image. Ensure they both have the `NET_ADMIN` capability.

```bash
docker compose up -d
```

Verify they can ping each other normally on the underlay network:
```bash
docker compose exec host-a ping -c 2 172.50.0.20
```

### Task 2 — Implement VLANs (802.1Q)

Even though they share the same physical-equivalent bridge, we can isolate them using VLAN tags. We will assign them to VLAN ID 100 with a new IP subnet (`10.100.0.0/24`).

1. Attach to `host-a` and create a VLAN sub-interface on `eth0`:
```bash
docker compose exec -u root host-a bash
# Inside host-a:
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 10.100.0.10/24 dev eth0.100
ip link set eth0.100 up
exit
```

2. Do the corresponding setup on `host-b`:
```bash
docker compose exec -u root host-b bash
# Inside host-b:
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 10.100.0.20/24 dev eth0.100
ip link set eth0.100 up
exit
```

3. Test Connectivity over the VLAN:
```bash
# Ping the VLAN interface of host-b from host-a
docker compose exec host-a ping -c 2 10.100.0.20
```
✅ **Success!** The traffic is now tagged with VLAN 100.

4. Verify isolation by using `tcpdump`.
Open a second terminal and capture traffic on `host-b`'s main interface (`eth0`):
```bash
docker compose exec host-b tcpdump -i eth0 -n -e vlan
```
While that runs, ping from `host-a` again in the first terminal. You should see 802.1Q tags in the capture!

### Task 3 — Setup a VXLAN Tunnel (Overlay)

Now let's build an L2 tunnel between `host-a` and `host-b` using VXLAN. We will use a new subnet: `192.168.99.0/24`. We set the VXLAN Network Identifier (VNI) to `42`.

1. On `host-a`, create the VXLAN interface. Notice that we tell it the `remote` IP endpoint (the underlay IP of host-b):
```bash
docker compose exec -u root host-a bash
ip link add vxlan42 type vxlan id 42 remote 172.50.0.20 dstport 4789 dev eth0
ip addr add 192.168.99.10/24 dev vxlan42
ip link set vxlan42 up
exit
```

2. On `host-b`, do the mirror configuration:
```bash
docker compose exec -u root host-b bash
ip link add vxlan42 type vxlan id 42 remote 172.50.0.10 dstport 4789 dev eth0
ip addr add 192.168.99.20/24 dev vxlan42
ip link set vxlan42 up
exit
```

3. Test the Overlay:
```bash
docker compose exec host-a ping -c 2 192.168.99.20
```
✅ **Success!** You just pinged over the overlay network.

4. Verify Encapsulation
In one terminal, listen for UDP traffic on the standard VXLAN port (4789) on the underlay:
```bash
docker compose exec host-b tcpdump -i eth0 -n udp port 4789
```
In another, send the ping again. You will see traffic encapsulated in UDP.

---

## ✅ Checklist

- [ ] Un-tagged underlay connectivity
- [ ] 802.1Q sub-interfaces and VLAN tagging isolation
- [ ] Captured traffic showing 802.1Q headers
- [ ] Creation of a point-to-point VXLAN overlay
- [ ] Captured traffic showing L2 over UDP encapsulation

---

## 🧹 Cleanup
```bash
docker compose down
```
