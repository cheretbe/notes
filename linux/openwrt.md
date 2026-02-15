```shell
nmcli con show | grep -i ether
CONNECTION_UUID="connection-uuid"
nmcli connection modify $CONNECTION_UUID ipv4.route-metric 700
nmcli connection down $CONNECTION_UUID
nmcli connection up $CONNECTION_UUID
# Here we assume that the connection has 2 IP addresses configured
# ipv4.addresses: 192.168.1.10/24, 192.168.88.10/24
nmcli -f ipv4.addresses connection show $CONNECTION_UUID

IF_NAME=enp0s31f6
# --port=0 disables DNS (DHCP/TFTP only)
dnsmasq --no-daemon --port=0 --enable-tftp --tftp-root=$(pwd) --interface=$IF_NAME \
  --dhcp-range=interface:$IF_NAME,192.168.88.100,192.168.88.200,12h --dhcp-host=cc:2d:e0:a2:f5:4f,192.168.88.50 --bootp-dynamic \
  --dhcp-boot=openwrt-24.10.5-ipq40xx-mikrotik-mikrotik_hap-ac2-initramfs-kernel.bin
```
