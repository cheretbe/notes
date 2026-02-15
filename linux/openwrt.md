### Microtic
* https://openwrt.org/toh/mikrotik/common
    * https://openwrt.org/toh/mikrotik/hap_ac2 
    * https://firmware-selector.openwrt.org/?version=24.10.5&target=ipq40xx%2Fmikrotik&id=mikrotik_hap-ac2
    * https://radiusdesk.com/docuwiki/user_guide/mikrotik/openwrt_rb750gr3
    * https://gist.github.com/bramford/781321e4cfd726730b68bb3adee36fa9
* TL/DR
    * :warning: Make backup of license key (Windows Winbox only :shrug:): System > License > Export Key...
    * Downgrade to ROS 6 (version 7 bootloader support is introduced in v25)
    * Don't forget that netboot is done on port 1, router conifg is on ports 2-5

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
# [!] connect to router's port 1
dnsmasq --no-daemon --port=0 --enable-tftp --tftp-root=$(pwd) --interface=$IF_NAME \
  --dhcp-range=interface:$IF_NAME,192.168.88.0,static --dhcp-host=cc:2d:e0:a2:f5:4f,192.168.88.50 --bootp-dynamic \
  --dhcp-boot=openwrt-24.10.5-ipq40xx-mikrotik-mikrotik_hap-ac2-initramfs-kernel.bin

# [!] connect to router's port 2-5
# user root, password is empty
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@192.168.1.1
```
