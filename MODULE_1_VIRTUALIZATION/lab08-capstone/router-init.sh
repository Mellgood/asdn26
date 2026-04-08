#!/bin/bash
echo "Starting Router"

# IP Forwarding
sysctl -w net.ipv4.ip_forward=1

# Default route to Firewall (172.20.1.253)
ip route del default
ip route add default via 172.20.1.253
