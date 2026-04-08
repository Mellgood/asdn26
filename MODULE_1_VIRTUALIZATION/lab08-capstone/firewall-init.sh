#!/bin/bash
echo "Starting Firewall"

# IP Forwarding
sysctl -w net.ipv4.ip_forward=1

# Static route to internal network via Router (172.20.1.254)
ip route add 172.20.2.0/24 via 172.20.1.254

# NAT Masquerade on external interface
EXT_IF="eth0"
iptables -t nat -A POSTROUTING -o $EXT_IF -j MASQUERADE

# Firewall Rules
iptables -F
iptables -P FORWARD DROP

# 1. ESTABLISHED, RELATED
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 2. Internal -> Internet (from 172.20.2.0/24 to external IF)
iptables -A FORWARD -i eth2 -o eth0 -s 172.20.2.0/24 -m conntrack --ctstate NEW -j ACCEPT

# 3. Internal -> DMZ
iptables -A FORWARD -s 172.20.2.0/24 -d 172.20.1.0/24 -m conntrack --ctstate NEW -j ACCEPT

# Note: DMZ is not allowed to initiate connections to Internal, because
# of the DROP policy and the absence of an explicit ACCEPT rule.
