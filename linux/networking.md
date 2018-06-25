```shell
brctl addbr test-br
brctl addif test-br ifname

# Get DHCP address
dhclient -v test-br
# Release
dhclient -v -r test-br

# ifdown test-br won't work since we don't use /etc/network/interfaces
ip link set dev test-br down
brctl delif test-br ifname
brctl delbr test-br
```

### Disable IPv6
Check status
```
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
```
Should return `1` if IPv6 is disabled

To disable, add the following to `/etc/sysctl.conf`
```
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
```
Apply changes
```
sudo sysctl -p
```
### Config examples
Ubuntu (/etc/network/interfaces)
```
# interface without an IP address
auto eth0
iface eth0 inet manual
  up ifconfig $IFACE 0.0.0.0 up
  down ifconfig $IFACE down
```

```
route delete -net 192.168.101.0/24 gw 192.168.99.11
route add -net 192.168.101.0/24 gw 192.168.100.9
```

WLAN
```
iwconfig
apt install wpasupplicant
```
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp1s0:
      dhcp4: yes
  wifis:
    wlp2s0:
      dhcp4: yes
      access-points:
        "name":
          password: "pwd"
```

* https://netplan.io/design#complex-example
* https://askubuntu.com/questions/63456/waiting-for-network-configuration-adding-3-to-5-minutes-to-boot-time/914479#914479
* https://www.linuxbabe.com/command-line/ubuntu-server-16-04-wifi-wpa-supplicant
* https://wiki.debian.org/BridgeNetworkConnections#Bridging_with_a_wireless_NIC
* https://github.com/GNS3/gns3-gui/issues/2348
* https://askubuntu.com/questions/155041/bridging-loosing-wlan-network-connection-with-4addr-on-option-why/207588#207588
* http://nullroute.eu.org/~grawity/journal-2011.html#post:20110826
