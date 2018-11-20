* https://nmap.org/book/man-host-discovery.html

```shell
# Lookup all IPs in a network
# -sn (No port scan), often known as a "ping scan"
# In previous releases of Nmap, -sn was known as -sP
# It's fast, but doesn't find all hosts
nmap -sn 192.168.1.0/24
nmap -sP 192.168.1.0/24
# Use ARP ping instead (takes long time)
nmap -PR 192.168.1.0/24
# View all IPs (including those who didn't reply on ping)
arp -a -n

# arp-scan if much faster and sorts output by IP
arp-scan 192.168.1.0/24
# then just use nmap to find out more about particular host
nmap 192.168.1.1
```
