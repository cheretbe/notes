* multiple wans
    * https://www.reddit.com/r/openwrt/comments/tuin03/trying_to_set_up_two_wans_on_one_router/
    * https://openwrt.org/docs/guide-user/network/wan/multiwan/mwan3?s[]=ipv6&s[]=setup
    * https://forum.openwrt.org/t/mwan3-documentation-simple-example/237699/4
    * https://oldme.knnect.com/blogs/openwrt_mwan3/
* backup
    * https://www.reddit.com/r/openwrt/comments/vuw59b/openwrt_backup/
    * https://openwrt.org/docs/guide-user/troubleshooting/backup_restore?s[]=open&s[]=level
* vpn
    * https://docs.amnezia.org/documentation/instructions/openwrt-os-awg/


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
# [!] initramfs-kernel, not squashfs-sysupgrade
#    easy way to find out router's MAC: just temporarily remove --dchp-host option altogether and wait for messages like
#    dnsmasq-dhcp: BOOTP(enp0s31f6) 00:00:00:00:00:00 no address configured
dnsmasq --no-daemon --port=0 --enable-tftp --tftp-root=$(pwd) --interface=$IF_NAME \
  --dhcp-range=interface:$IF_NAME,192.168.88.0,static --dhcp-host=00:00:00:00:00:00,192.168.88.50 --bootp-dynamic \
  --dhcp-boot=openwrt-24.10.5-ipq40xx-mikrotik-mikrotik_hap-ac2-initramfs-kernel.bin

# [!] connect to router's port 2-5
# user root, password is empty
# [!] squashfs-sysupgrade, not initramfs-kernel
# Or go to "System" > "Backup / Flash Firmware" in the UI
scp -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  openwrt-24.10.5-ipq40xx-mikrotik-mikrotik_hap-ac2-squashfs-sysupgrade.bin root@192.168.1.1:/tmp/
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@192.168.1.1

cd /tmp
sysupgrade openwrt-24.10.5-ipq40xx-mikrotik-mikrotik_hap-ac2-squashfs-sysupgrade.bin
```
