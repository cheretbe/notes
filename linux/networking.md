```shell
# Temporarily enable routing
echo 1 > /proc/sys/net/ipv4/ip_forward

# Permanently store the setting:
# Uncomment 'net.ipv4.ip_forward=1' line in /etc/sysctl.conf
# And re-read kernel parameters
sysctl -p /etc/sysctl.conf

# NAT
iptables --table nat --append POSTROUTING -s 192.168.1.0/24 --out-interface ifname -j MASQUERADE

# Capture ICMP packets on an interface
# -n     Don't convert addresses (i.e., host addresses, port numbers, etc.) to names
tcpdump -n -i ifname icmp
```

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

Ubuntu 18.04:
* https://askubuntu.com/questions/1046057/disabling-ipv6-in-ubuntu-18-04-server/1046648#1046648
* https://askubuntu.com/questions/575651/what-is-the-difference-between-grub-cmdline-linux-and-grub-cmdline-linux-default

### Config examples
Ubuntu (/etc/network/interfaces)
```
# interface without an IP address
auto eth0
iface eth0 inet manual
  up ifconfig $IFACE 0.0.0.0 up
  down ifconfig $IFACE down
  
# allow-hotplug eth1
# auto eth1
iface eth1 inet static
	  address 192.168.1.4
	  netmask 255.255.255.0
	  network 192.168.1.0
	  broadcast 192.168.1.255
	  gateway 192.168.1.1
	  # dns-* options are implemented by the resolvconf package, if installed
	  dns-nameservers 192.168.1.1
```
Ubuntu Netplan (/etc/netplan/01-netcfg.yaml)
```yaml
network:
 version: 2
 renderer: networkd
 ethernets:
   eth0:
     dhcp4: false
   eth1:
     dhcp4: true
     # Will speed up boot process if there is no DHCPv6 server available
     dhcp6: no
     # Disable waiting for interface to fully activate
     optional: true
 bridges:
   br0:
     interfaces: [eth0]
     dhcp4: false
     addresses: [192.168.1.99/24]
     gateway4: 192.168.1.1
     nameservers:
       addresses: [1.1.1.1,8.8.8.8]
     parameters:
       forward-delay: 0
```
```shell
# Apply configuration
sudo netplan generate
sudo netplan apply
# View debug info
sudo netplan --debug apply
networkctl list
ifconfig
```

:question: Debian Jessie(8) and Stretch(9) by default use `/etc/dhcpcd.conf` instead of `/etc/network/interfaces` - https://raspberrypi.stackexchange.com/questions/39785/dhcpcd-vs-etc-network-interfaces/41187#41187

### Routes
```
route delete -net 192.168.101.0/24 gw 192.168.99.11
route add -net 192.168.101.0/24 gw 192.168.100.9
```
### DNS
```shell
systemd-resolve --status
```

### WLAN
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
