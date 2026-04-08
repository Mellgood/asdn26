#!/bin/bash
# Router Initialization Script

echo "Initializing Router..."

# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1

echo "IP forwarding enabled."
