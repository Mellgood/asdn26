# Lab 09 — Interfaces and Namespaces Deep Dive

## 🎯 Objective

Understand the lower-level mechanics of network isolation in Linux. You will learn how to inspect physical vs virtual network hardware, manually create Linux Network Namespaces, build Virtual Ethernet pairs (`veth`), and bridge them together — effectively replicating the core magic of Docker containers from scratch.

> ⚠️ **CRITICAL REQUIREMENT:** 
> Do **NOT** run these commands on your host Mac or Windows terminal. Docker Desktop hides its Linux kernel in a private VM. You must run this entire lab **inside** the Multipass `asdn-node` Virtual Machine created in **Lab 00**.

---

## 🔬 Tasks

### Task 1 — Access the Lab VM & Install Tools

1. Open a terminal on your host machine and log into your VM:
   ```bash
   multipass shell asdn-node
   ```

2. Install the necessary low-level Linux networking unilities:
   ```bash
   sudo apt update
   sudo apt install -y lshw pciutils net-tools ethtool
   ```

### Task 2 — Physical vs Virtual Interfaces

Let's inspect the network interfaces that the Hypervisor provides to our Ubuntu OS.

1. **List hardware with `lshw`**:
   ```bash
   sudo lshw -c network -short
   ```
   > 📝 **Question:** What is the class and description of the device? Does it look like physical hardware or is it explicitly named as a virtual device (e.g., virtio)?

2. **Inspect capabilities with `ethtool`**:
   Find the name of your primary interface (usually `ens3`, `eth0`, or `enp0s3`). Use `ip link` to verify. Then:
   ```bash
   sudo ethtool <interface_name>
   ```
   > 📝 **Question:** What is the "Speed" of the interface? Are properties like "Link detected" set to yes?

### Task 3 — Linux Network Namespaces (`ip netns`)

A namespace provides a completely isolated network stack.

1. List current namespaces (should be empty):
   ```bash
   ip netns list
   ```

2. Create a new namespace named `blue`:
   ```bash
   sudo ip netns add blue
   ```

3. Execute a command *inside* the namespace:
   ```bash
   sudo ip netns exec blue ip addr
   ```
   > 📝 **Question:** What interfaces exist inside the `blue` namespace? Notice how the primary `eth0` of the VM is missing!

4. Turn on the loopback interface inside the namespace:
   ```bash
   sudo ip netns exec blue ip link set lo up
   sudo ip netns exec blue ping -c 1 127.0.0.1
   ```

### Task 4 — The `veth` Cable

We have an isolated namespace (`blue`), but it's completely disconnected from the world. We need a virtual cable.

1. Create a `veth` pair. A `veth` pair always has two ends. We will name them `veth-host` and `veth-blue`:
   ```bash
   sudo ip link add veth-host type veth peer name veth-blue
   ```

2. Verify they exist in the root (host) namespace:
   ```bash
   ip link
   ```
   You will see both components linked together via `@`.

3. Move the `veth-blue` end **into** the `blue` namespace:
   ```bash
   sudo ip link set veth-blue netns blue
   ```

4. Verify it moved! It is no longer in the host `ip link`, but it is inside the namespace:
   ```bash
   sudo ip netns exec blue ip link
   ```

### Task 5 — Assign IPs and Test Connectivity

Now we configure the interfaces like real network adapters.

1. Assign an IP to the host side and turn it up:
   ```bash
   sudo ip addr add 10.99.0.1/24 dev veth-host
   sudo ip link set veth-host up
   ```

2. Assign an IP to the namespace side and turn it up:
   ```bash
   sudo ip netns exec blue ip addr add 10.99.0.2/24 dev veth-blue
   sudo ip netns exec blue ip link set veth-blue up
   ```

3. **The Moment of Truth**: Can the host ping the isolated namespace?
   ```bash
   ping -c 3 10.99.0.2
   ```
   ✅ **Success!** You have just created a highly isolated process environment with custom networking. Docker automates these exact `ip netns` and `ip link` commands every time you type `docker run`.

### Task 6 (Bonus) — Inspecting Virtual Offload

Docker relies heavily on `veth` pairs. Let's see how fast they are.

```bash
sudo ethtool -k veth-host | grep offload
```
You will notice many offload features (like tcp-segmentation-offload) are turned `on`. The Linux kernel optimizes `veth` traffic so deeply that it bypasses standard MTU limits and hardware checksums, passing large chunks of memory directly between namespaces for extreme performance.

---

## 🧹 Cleanup

Since we created these structures manually (and not via a container runtime), they persist until reboot. Let's clean them up.

```bash
# Deleting the namespace automatically destroys the veth-blue interface inside it.
# Deleting one end of a veth pair (veth-blue) automatically destroys the other end (veth-host).
sudo ip netns delete blue
```

Type `exit` to leave the `asdn-node` VM and return to your host terminal.

---

## ✅ Checklist

- [ ] Used `lshw` and `ethtool` to examine network hardware
- [ ] Created a manual Linux Network Namespace
- [ ] Plumbed a `veth` pair between the host root namespace and the custom namespace
- [ ] Established routing between the host and the namespace
