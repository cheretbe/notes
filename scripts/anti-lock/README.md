```shell
./amazon_ips.py ~/temp/amazon_nets.rsc
/import amazon_nets.rsc

# Delete all rules
/ip/firewall/address-list/ remove [/ip/firewall/address-list/ find comment~"^<auto Amazon>"]
```