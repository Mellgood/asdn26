#!/bin/bash
# Firewall Initialization Script

echo "Initializing Firewall..."

# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1

# Clear existing iptables rules
iptables -F
iptables -t nat -F

# Find the external interface (connected to the default network)
# Since the others are defined with subnets, we assume eth0 is the external one.
# If not, you might need to extract the interface name via:
# EXT_IF=$(ip -4 route ls | grep default | grep -Po '(?<=dev )(\S+)')
EXT_IF="eth0"

# Add Masquerade rule for all outgoing traffic on the external interface
iptables -t nat -A POSTROUTING -o $EXT_IF -j MASQUERADE

# Set default FORWARD policy to DROP
iptables -P FORWARD DROP

# Allow ESTABLISHED/RELATED connections
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow NEW connections from Internal (assuming 172.40.2.0/24 is internal)
iptables -A FORWARD -s 172.40.2.0/24 -m conntrack --ctstate NEW -j ACCEPT

# (Optional Challenge) Add DNAT rule from external port 80 to web-server
iptables -t nat -A PREROUTING -i $EXT_IF -p tcp --dport 80 -j DNAT --to-destination 172.40.1.10:80
# Explicitly allow this DNAT traffic through the FORWARD chain
iptables -A FORWARD -d 172.40.1.10 -p tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT

echo "Firewall rules applied."
