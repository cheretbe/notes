```shell
# WG server

# Uncomment 'net.ipv4.ip_forward=1' line in /etc/sysctl.conf
# And re-read kernel parameters
sysctl -p /etc/sysctl.conf
# View current setting
cat /proc/sys/net/ipv4/ip_forward

iptables -A FORWARD -i wg0 -o wg0 -j ACCEPT


# LAN router

echo 1 > /proc/sys/net/ipv4/ip_forward
# Uncomment 'net.ipv4.ip_forward=1' line in /etc/sysctl.conf
# And re-read kernel parameters
sysctl -p /etc/sysctl.conf
# View current setting
cat /proc/sys/net/ipv4/ip_forward
iptables --table nat --append POSTROUTING -s 192.168.101.0/24 --out-interface wg-hub -j MASQUERADE
```
