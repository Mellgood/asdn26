#!/bin/bash
# Firewall Initialization Script

echo "Initializing Firewall..."

# 1. Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1

# 2. Clear existing iptables rules (optional, good for idempotency)
iptables -F
iptables -t nat -F

# TODO: Add Masquerade rule for outgoing traffic
# ...

# TODO: Set default FORWARD policy to DROP
# ...

# TODO: Add Accept rules for ESTABLISHED/RELATED and NEW from Internal
# ...

# TODO (Optional Challenge): Add DNAT rule from external port 80 to web-server
# ...

echo "Firewall rules applied."
