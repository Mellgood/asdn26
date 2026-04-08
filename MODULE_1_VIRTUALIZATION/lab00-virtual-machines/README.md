# Lab 00 — Virtual Machines Basics (Hardware-Level Virtualization)

## 🎯 Objective

Before diving into OS-level virtualization (Docker containers), we must understand traditional hardware-level virtualization (Virtual Machines). By the end of this lab, you will have deployed a full Linux Ubuntu Virtual Machine on your local computer using **Canonical Multipass**.

This VM will be your "bare-metal" equivalent for exploring low-level Linux networking later in the course.

## 📖 Background

### Why Multipass instead of VirtualBox?
Historically, courses used VirtualBox or VMware. However, with the transition to ARM processors (like Apple's M1/M2/M3 chips), traditional x86-based tools like VirtualBox fail to run or emulate poorly natively on Mac.

**Multipass** solves this. It relies on the native hypervisor of your operating system:
- **Windows**: Hyper-V or VirtualBox
- **macOS**: Hypervisor.framework (native Apple silicon support)
- **Linux**: KVM (Kernel Virtual Machine)

Multipass automatically downloads a clean Ubuntu image compiled for your specific CPU architecture (AMD64 or ARM64) and launches it in seconds.

---

## 🔬 Tasks

### Task 1 — Install Multipass

1. Go to the [official Multipass website](https://multipass.run/).
2. Download and install the version for your Operating System.
3. Open your terminal (PowerShell on Windows, Terminal on Mac/Linux) and verify the installation:
   ```bash
   multipass version
   ```

### Task 2 — Launch Your First VM

We will create a VM named `asdn-node` with 2 CPUs, 2GB of RAM, and 10GB of disk space.

1. Launch the VM:
   ```bash
   multipass launch --name asdn-node --cpus 2 --memory 2G --disk 10G
   ```
   *(Note: The first launch might take a couple of minutes as it downloads the Ubuntu image.)*

2. Verify it is running:
   ```bash
   multipass list
   ```
   > 📝 **Question:** What is the IPv4 address assigned to your `asdn-node`? 

### Task 3 — Access the VM

To log into your virtual machine, use the `shell` command. Multipass handles the SSH key exchange automatically.

1. Open a shell inside the VM:
   ```bash
   multipass shell asdn-node
   ```
   You should see your prompt change to: `ubuntu@asdn-node:~$`. You are now inside a full Linux environment!

### Task 4 — Explore the Virtual Hardware

Is this a real computer? From the OS perspective, yes! Let's explore the virtualized hardware.

1. **Check the CPU**:
   ```bash
   lscpu
   ```
   > 📝 **Question:** What is the Architecture? (It will be `x86_64` on Intel/AMD or `aarch64` on Apple Silicon).

2. **Check the RAM**:
   ```bash
   free -h
   ```

3. **Check the Disk Space**:
   ```bash
   df -h /
   ```

4. **Exit the VM**:
   Type `exit` or press `Ctrl + D` to return to your host terminal.

### Task 5 — VM Lifecycle Management

Learn how to manage your VM:

1. **Stop the VM**:
   ```bash
   multipass stop asdn-node
   multipass list
   ```

2. **Start it again**:
   ```bash
   multipass start asdn-node
   ```

*(Do not delete the VM, you will need it for Lab 09!)*

---

## ✅ Checklist

- [ ] Installed Canonical Multipass
- [ ] Deployed an Ubuntu virtual machine
- [ ] Accessed the VM shell natively
- [ ] Explored CPU and memory limits inside the VM

---

## 📚 Further Reading
- [Multipass Documentation](https://multipass.run/docs)
- [Hypervisor vs Container Overview](https://www.docker.com/resources/what-container)
