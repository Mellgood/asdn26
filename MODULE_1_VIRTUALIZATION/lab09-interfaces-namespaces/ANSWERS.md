# Lab 09 — Interfaces and Namespaces Deep Dive: Answers

## Task 2
> **What is the class and description of the device? Does it look like physical hardware or is it explicitly named as a virtual device (e.g., virtio)?**
If running under Multipass, the class is usually `network` and the description is often `Ethernet interface` but the driver or product name typically gives it away as `Virtio network device` or `Hyper-V virtual network adapter`. It is a para-virtualized device.

> **What is the "Speed" of the interface? Are properties like "Link detected" set to yes?**
The speed reported is often arbitrarily high (e.g. `10000Mb/s` or `Unknown!`) because it is a virtual construct with no real physical speed limit other than CPU and RAM bandwidth. "Link detected" will be `yes`.

## Task 3
> **What interfaces exist inside the blue namespace?**
Only the `lo` (loopback) interface exists, and its state is `DOWN` by default. Everything else is completely isolated.
