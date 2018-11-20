```shell
# Lookup all IPs in a network
# -sn (No port scan), often known as a “ping scan”
# In previous releases of Nmap, -sn was known as -sP
nmap -sP 192.168.1.0/24
# View all IPs (including those who didn't reply on ping)
arp -a -n
```
