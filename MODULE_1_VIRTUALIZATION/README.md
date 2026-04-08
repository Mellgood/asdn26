# Module 1 — Virtualization

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain the difference between hardware-level and OS-level virtualization
- Use Docker to build, run, and manage containers
- Write Dockerfiles to create custom images
- Understand Docker's networking model (bridge, host, none)
- Inspect and manipulate virtual network interfaces (veth pairs, bridges)
- Use Docker Compose to orchestrate multi-container environments
- Configure a container as a **router** between isolated networks
- Configure a container as a **firewall** with iptables rules and NAT
- Work with VLANs and overlay networks (VXLAN) inside containers
- Build a realistic multi-segment network topology entirely in Docker

## 🗺️ Lab Overview

| Lab | Title | Difficulty | Topics |
|-----|-------|------------|--------|
| [Lab 01](lab01-docker-basics/) | Docker Basics | ⭐ | CLI, containers, images, port mapping |
| [Lab 02](lab02-images-and-dockerfiles/) | Images & Dockerfiles | ⭐ | Dockerfile, layers, custom images, net-tools |
| [Lab 03](lab03-docker-networking-fundamentals/) | Docker Networking Fundamentals | ⭐⭐ | Bridge, host, none, veth pairs, DNS |
| Lab 04 | Docker Compose & Multi-Container Apps | ⭐⭐ | Compose, service networks, isolation |
| Lab 05 | Container as a Router | ⭐⭐⭐ | IP forwarding, routing, multi-homed containers |
| Lab 06 | Container as a Firewall / NAT Gateway | ⭐⭐⭐ | iptables, NAT, DNAT, DMZ |
| Lab 07 | VLAN and Overlay Networks | ⭐⭐⭐ | 802.1Q, VXLAN, overlay drivers |
| Lab 08 | Multi-Segment Network Topology | ⭐⭐⭐⭐ | Capstone: full enterprise topology |

## 📋 Prerequisites

- Docker Engine (v20.10+) or Docker Desktop installed and running
- Basic familiarity with the Linux command line
- A text editor (VS Code recommended)

## 🚀 Getting Started

Start with [Lab 01 — Docker Basics](lab01-docker-basics/) and work your way through sequentially.

> **Note:** Each lab builds on the previous one. The custom `net-tools` image you create in Lab 02 will be used extensively in Labs 03–08.
