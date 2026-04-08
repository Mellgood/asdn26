# Lab 00 — Virtual Machines Basics: Answers

## Task 2
> **What is the IPv4 address assigned to your asdn-node?**
The IP address is dynamically assigned by the hypervisor's DHCP server (e.g. `192.168.64.x` on macOS, or `172.x.x.x` on Windows Hyper-V).

## Task 4
> **What is the Architecture?**
Depends on the host machine. If you are on an Apple Silicon Mac, it will be `aarch64`. If you are on Windows/Intel, it will be `x86_64`. Multipass automatically fetches the correct Ubuntu image for the host architecture.
