#!/bin/bash

# Flush existing rules
iptables -F
iptables -X

# Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow outgoing DNS
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

# Allow outgoing NTP
iptables -A OUTPUT -p udp --dport 123 -j ACCEPT

# Allow outgoing HTTP/HTTPS only through Tor
iptables -A OUTPUT -p tcp --dport 80 -m owner --uid-owner debian-tor -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -m owner --uid-owner debian-tor -j ACCEPT

# Allow Tor traffic
iptables -A OUTPUT -p tcp --dport 9050 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 9051 -j ACCEPT

# Block all other outgoing traffic
iptables -A OUTPUT -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4