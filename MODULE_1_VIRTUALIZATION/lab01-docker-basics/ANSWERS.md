# Lab 01 — Docker Basics: Answers

## Task 1 — Verify Your Docker Installation

> **What storage driver does your Docker installation use?**

Typically `overlay2` on modern Docker installations.

> **What operating system is Docker running on?**

On macOS/Windows: Docker Desktop runs a lightweight Linux VM (e.g., `Docker Desktop` or `Alpine Linux`).
On Linux: Your host Linux distribution directly.

---

## Task 2 — Hello World

> **Why is the second `docker run hello-world` faster than the first?**

Because the image is already cached locally. Docker doesn't need to pull it from Docker Hub again. It only needs to create the container and run it.

---

## Task 3 — Interactive Container

> **How many processes are running inside the container? How does that compare to your host machine?**

Inside the container, `ps aux` typically shows only 1-2 processes (the shell `sh` and `ps` itself). On the host, there are hundreds of processes. This demonstrates the process isolation provided by Linux namespaces.

---

## Task 6 — Container Inspection

> **What IP address was assigned to the container? What network is it on?**

The container gets an IP address on the default `bridge` network, typically in the `172.17.0.0/16` range (e.g., `172.17.0.2`). The network name is `bridge`.

---

## Task 8 — Execute Commands in a Running Container

> **What is the default gateway of the container? What does it correspond to?**

The default gateway is `172.17.0.1` (the gateway of the default bridge network). This is the IP address of the `docker0` bridge interface on the host. All outbound traffic from the container goes through this gateway, where Docker's iptables rules handle NAT to allow internet access.
