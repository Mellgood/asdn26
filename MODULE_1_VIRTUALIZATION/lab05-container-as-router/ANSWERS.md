# Lab 05 — Container as a Router

## Task 2
> **Why does the ping to Host-B fail?**
There are two reasons:
1. `host-a`'s routing table lacks a route to `net-beta` (`10.5.2.0/24`), so it sends the packet to its default gateway (the docker bridge gateway), which drops the unknown private IP.
2. Even if it reached the `router` container, the `router`'s kernel has `net.ipv4.ip_forward=0`, so it drops packets not destined for its own IP.
