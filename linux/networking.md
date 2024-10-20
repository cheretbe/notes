* :point_right: `apt install nethogs`
* iptraf-ng: https://github.com/iptraf-ng/iptraf-ng/
* `ip` command cheatsheet: https://access.redhat.com/sites/default/files/attachments/rh_ip_command_cheatsheet_1214_jcs_print.pdf

```shell
# dig may return canonical names for if CNAME records are present. grep filters them out
dig +short registry.terraform.io | grep -v '\.$' | xargs -I % ip route add % via 192.168.88.3 metric 50

# Physical interfaces info (note the H/W path)
lshw -class network -short
# Note a device name and find out detailed info
lshw -class network
# TODO: researsh -json key and jq queries

# ip -br -c a
# ip -br -c link

ip link show
# Display information only for one device
ip link show dev <ifname>

# Bring an interface up/down
ip link set dev <ifname> up
ip link set dev <ifname> down

# Detect link on interfaces ([!] brings up all available interfaces)
for if in $(ls /sys/class/net -I lo); do echo -n "$if: "; sleep 1; ip link set dev $if up; (ethtool $if | grep -i "Link detected:"); done

# view IP(s)
hostname -I
ip addr

# View interfaces (note "state UP" or "state DOWN")
ipconfig -a

# Test port access
nc -l -p 1234
echo "Test" | nc host.domain.tld 1234
# Test UDP broadcast
echo "UDP broadcast" | socat - UDP4-DATAGRAM:192.168.1.255:12345,so-broadcast
nc -l -u 12345

# Temporarily enable routing
echo 1 > /proc/sys/net/ipv4/ip_forward

# Permanently store the setting:
# Uncomment 'net.ipv4.ip_forward=1' line in /etc/sysctl.conf
# And re-read kernel parameters
sysctl -p /etc/sysctl.conf

# View current setting
cat /proc/sys/net/ipv4/ip_forward

# Capture ICMP packets on an interface
# -n     Don't convert addresses (i.e., host addresses, port numbers, etc.) to names
tcpdump -n -i ifname icmp
# On all interfaces
tcpdump -n -i any icmp
# On port 80
tcpdump -n -i eth0 'tcp port 80'
# On all ports except for 22 (useful when connected via SSH)
tcpdump -n -i any 'port not 22'
# 636 - LDAP
# 514 - rsyslog
# 53  - DNS
# 25  - SMTP
tcpdump -n -i ens160 dst host 10.0.176.79 and not src port 514 and not src port 53 and not src port 636 and not src port 25 and not arp and not llc
# [!!!] Try running with tee

# To display names of interfaces tcpdump has to be 4.99 or greater
# https://serverfault.com/questions/224698/how-to-display-interface-in-tcpdump-output-flow/1054024#1054024
# If the version shipped with OS is lower, download the latest one from https://www.tcpdump.org/ and build it
apt install build-essential flex bison

wget https://www.tcpdump.org/release/libpcap-1.10.1.tar.gz
tar xzvf libpcap-1.10.1.tar.gz 
cd libpcap-1.10.1/
./configure && make

cd ..
wget https://www.tcpdump.org/release/tcpdump-4.99.1.tar.gz
tar xzvf tcpdump-4.99.1.tar.gz
cd tcpdump-4.99.1/
./configure && make

./tcpdump
./tcpdump -n -i any icmp
```

```shell
ifconfig ifname 0.0.0.0 up
brctl addbr test-br
brctl addif test-br ifname
brctl show

ifconfig test-br 172.24.0.1/24 up
# Or get DHCP address
dhclient -v test-br
# Release
dhclient -v -r test-br

# ifdown test-br won't work since we don't use /etc/network/interfaces
ifconfig test-br down
ip link set dev test-br down

brctl delif test-br ifname
brctl delbr test-br
```

### iptables
* :bulb: https://www.digitalocean.com/community/tutorials/how-to-list-and-delete-iptables-firewall-rules
* Both iptables and nftables are interfaces to configure netfilter (Linux kernel subsystem). nftables iptables.
```shell
# NAT
iptables --table nat --append POSTROUTING -s 192.168.1.0/24 --out-interface ifname -j MASQUERADE
# Use --verbose to view out interfaces
iptables --verbose --list --table nat
# Short form
iptables -vL -t nat
# Or just use iptables-save to view all rules in detail
iptables-save

iptables --table nat --delete POSTROUTING -s 192.168.1.0/24 --out-interface ifname -j MASQUERADE
# Destination NAT (DNAT)
iptables --table nat --append PREROUTING --in-interface ifname --protocol tcp --dport 80 -j DNAT --to 192.168.1.10:80

# Delete by chain and number (easier)
iptables -L --line-numbers
iptables -D INPUT 7

# Delete by specification (use iptables-save to find it out)
iptables -D INPUT -p tcp -m tcp --dport 1194 -m comment --comment "Allow VPN" -j ACCEPT

apt install iptables-persistent
iptables-save > /etc/iptables/rules.v4

# Reload
iptables-restore < /etc/iptables/rules.v4
```

#### Docker
* https://docs.docker.com/network/iptables/
All of Docker’s iptables rules are added to the DOCKER chain. Do not manipulate this chain manually. If you need to add rules which load before Docker’s rules, add them to the DOCKER-USER chain. These rules are applied before any rules Docker creates automatically.
```shell
iptables -I DOCKER-USER -i ext_if ! -s 192.168.1.0/24 -j DROP
iptables -L DOCKER-USER
# Docker also sets the policy for the FORWARD chain to DROP. If your Docker host also acts as a router,
# this will result in that router not forwarding any traffic anymore. If you want your system to continue
# functioning as a router, you can add explicit ACCEPT rules to the DOCKER-USER chain to allow it:
iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```

### Detect network renderer

* https://askubuntu.com/questions/1031439/am-i-running-networkmanager-or-networkd/1246465#1246465
```shell
nmcli dev status
networkctl list
service dhcpcd status
```
* [NetworkManager](#networkmanager)
* [systemd-networkd (networkd)](#systemd-networkd-networkd)
* [dhcpcd](#dhcpcd)

### NetworkManager
* * :warning: [Detect network renderer](#detect-network-renderer)
* https://developer.gnome.org/NetworkManager/stable/nmcli.html
* https://developer.gnome.org/NetworkManager/stable/nmcli-examples.html
* https://developer.gnome.org/NetworkManager/stable/NetworkManager.conf.html
* :point_right: https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html
* :warning: https://developer.gnome.org/NetworkManager/stable/nmtui.html (especially useful for Wi-Fi config)

```shell
# General info
nmcli -t -f RUNNING general
nmcli general
nmcli dev status

# View active connections
nmcli con show --active
# List Wi-Fi networks
nmcli dev wifi

# View ipv4 settings
nmcli -t --fields ipv4 con show <connectionName>
# View actual ipv4 parameters
nmcli -t --fields IP4 con show <connectionName>
# All devices
nmcli --fields IP4 dev show

# Rename a connection (change id - human-readable identifier)
nmcli connection modify "Wired connection 2" connection.id "ThinkPad USB dock"

# Modify settings for an existing connection
nmcli con mod <connectionName> ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod <connectionName> ipv4.ignore-auto-dns yes
# DHCP client ID
nmcli con mod <connectionName> ipv4.dhcp-client-id my-client-id
# reset to default (MAC address)
nmcli con mod <connectionName> ipv4.dhcp-client-id ""
# Apply changes
# (not necessary) nmcli con down <connectionName>
nmcli con up <connectionName>
```

Ubuntu 18.04. GUI doesn't have a menu to add VLANs
```shell
apt install vlan
nmcli con add type vlan ifname VLAN11-description dev enp0s31f6 id 11

nmcli con show
nmcli con show --active

nmcli con down conn-name
nmcli con up conn-name
```
OpenVPN plugin<br>
:warning: logon/logoff is needed
```shell
apt-get install network-manager-openvpn network-manager-openvpn-gnome
```
To import `.ovpn` file don't select `OpenVPN` menu item, use `Import from file...` at the bottom

### systemd-networkd (networkd)

* :warning: [Detect network renderer](#detect-network-renderer)
```shell
networkctl list
```

### dhcpcd
Tested on Raspberry Pi OS Lite (Debian 11) only
* :warning: [Detect network renderer](#detect-network-renderer)
```shell
# other terminal
ip monitor
ip monitor link
# this terminal
service dhcpcd restart

ip link set enp3s0 down
ip addr delete 192.168.0.50/24 dev enp3s0
```

`/etc/dhcpcd.conf` settings
```
# Use predictable interface names since this  is a space or comma separated
# list of patterns passed to fnmatch
denyinterfaces eth0

clientid "host.domain.tld"
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

RHEL, CentOS (/etc/sysconfig/network-scripts/)

By default, RHEL 7 and 8 use NetworkManager to configure and manage network connections,
and the `/usr/sbin/ifup` and `/usr/sbin/ifdown` scripts use NetworkManager to
process `ifcfg` files in the `/etc/sysconfig/network-scripts/` directory.

```shell
# Load a new configuration file
nmcli connection load /etc/sysconfig/network-scripts/ifcfg-connection_name
# After updating a connection file that has already been loaded into NetworkManager 
nmcli connection up connection_name 
```

* RHEL 8 - 5.4. Loading manually-created ifcfg files into NetworkManager: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/getting-started-with-networkmanager_configuring-and-managing-networking#loading-manually-created-ifcfg-files-into-networkmanager_getting-started-with-networkmanager
* RHEL 7 - 2.7. USING NETWORKMANAGER WITH SYSCONFIG FILES: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/sec-using_networkmanager_with_sysconfig_files

Opensuse (/etc/sysconfig/network)
```
# /etc/sysconfig/network/ifcfg-eth1
# DHCP
BOOTPROTO='dhcp'
STARTMODE='auto'
DEVICE='eth1'

# Static
BOOTPROTO='static'
IPADDR='172.24.0.1'
NETMASK='255.255.255.0'
DEVICE='eth1'
PEERDNS='no'
STARTMODE='auto'
USERCONTROL='no'


```

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
      # See also systemd-networkd-wait-online service timeout below
      optional: true
      #dhcp-identifier: mac
    enp0s3:
      dhcp4: true
      dhcp4-overrides:
        use-routes: false
        use-dns: false
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
* :warning: https://netplan.io/reference/
```shell
# View final config
netplan get

# Apply configuration
sudo netplan generate
# https://netplan.readthedocs.io/en/stable/netplan-try/
# Takes a configuration, applies it, and automatically rolls it back if the user does not
# confirm the configuration within a time limit
# [!!] Reverting custom parameters for bridges and bonds is not supported
#      try shows a message: "Please carefully review the configuration and use 'netplan apply' directly.
sudo netplan try

sudo netplan apply
# View debug info
sudo netplan --debug apply
networkctl list
ifconfig
```

Change timeout for "A start job is running for Wait For Network to be Configured":
```
systemctl edit  systemd-networkd-wait-online
```
```
[Service]
TimeoutStartSec=5sec
```

:question: Debian Jessie(8) and Stretch(9) by default use `/etc/dhcpcd.conf` instead of `/etc/network/interfaces` - https://raspberrypi.stackexchange.com/questions/39785/dhcpcd-vs-etc-network-interfaces/41187#41187<br>
`/etc/dhcpcd.conf` example:
```
interface eth0
static ip_address=10.1.1.30/24
static routers=10.1.1.1
static domain_name_servers=10.1.1.1
```
```shell
# Apply configuration
service dhcpcd restart
```


### Routes
```shell
route delete -net 192.168.101.0/24 gw 192.168.99.11
route add -net 192.168.101.0/24 gw 192.168.100.9
# add a route via an interface
route add -net 172.24.0.0/24 dev eth0

ip route add 192.168.1.0/24 via 192.168.0.1
# Change metric
# It's not possible to modify metric. Delete and recreate the route
ip route delete default via 192.168.1.1
ip route add default via 192.168.1.1 metric 90
```
### DNS
```shell
# Ubuntu with systemd-resolved enabled
resolvectl status
# RHEL/CentOS
nmcli --fields IP4.DNS dev show

# View DNS record TTL. If your default DNS server is not the authoritative server for the zone
# you will see the time remaining (until the next refresh) instead of the raw TTL value.
nslookup -debug host.domain.tld
nslookup -version
# In RedHat and Windows -debug option works, in Ubuntu it doesn't. Use dig
dig +nocmd +noall +answer host.domain.tld

# View SOA record
dig SOA +multiline domain.tld @192.168.0.1
nslookup -q=soa domain.tld
```
#### systemd-resolved

Fix for systemd-resolved not resolving `.local` names:

There are [four modes](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html#/etc/resolv.conf)
of handling `/etc/resolv.conf`. We select the third one (`/run/systemd/resolve/resolv.conf` symlinked from `/etc/resolv.conf`).

```shell
ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf

# As of systemd 232 DNS stub listener can be disabled
systemctl --version
# Create config override file
# [!] No, `systemctl edit systemd-resolved.service` won't work. It creates
# /etc/systemd/system/systemd-resolved.service.d/override.conf and [Resolve] section
# doesn't belong there
mkdir -p /etc/systemd/resolved.conf.d
cat <<EOF >/etc/systemd/resolved.conf.d/10-disable-dns-stub.conf
[Resolve]
DNSStubListener=no
EOF
systemctl restart systemd-resolved.service

# Restore default settings
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
rm /etc/systemd/resolved.conf.d/10-disable-dns-stub.conf
systemctl restart systemd-resolved.service
```
* https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html#/etc/resolv.conf
* https://www.freedesktop.org/software/systemd/man/resolved.conf.html
* https://github.com/systemd/systemd/issues/10298
* https://github.com/systemd/systemd/issues/2514

### DHCP
```shell
# Renew leases
dhclient -r; dhclient

# Systemd doesn't allow renewal
# https://lists.freedesktop.org/archives/systemd-devel/2014-August/022662.html
# restart the service instead
service systemd-networkd restart
```
Leases locations:
* `/var/lib/dhcp/dhclient.ifname.leases` file
* systemd: under `/run/systemd/netif/leases/`
```shell
# Change machine ID
mv /etc/machine-id{,.bak}
systemd-machine-id-setup
reboot
```
:information_source: `/var/lib/dbus/machine-id` is a symlink to `/etc/machine-id` (at least on Debian/Ubuntu it is). (https://unix.stackexchange.com/questions/402999/it-is-ok-to-change-etc-machine-id/403054#403054)<br>
:warning: TODO: Do some tests on Ubuntu/CentOS and update this section

### WLAN

* Diagnostics: https://www.cyberciti.biz/tips/linux-find-out-wireless-network-speed-signal-strength.html
* https://play.google.com/store/apps/details?id=com.vrem.wifianalyzer&hl=en_GB

```shell
# List network interfaces
ls -lha /sys/class/net
# List available Wi-Fi networks
iwlist wlp0s20f3 scan
# View status
iwconfig

apt install wpasupplicant
# [!] Add the line "p2p_disabled=1" in "/etc/wpa_supplicant/wpa_supplicant.conf" to disable the p2p interface
# List interfaces
wpa_cli interface
# View interface status
wpa_cli -i wlan0 status
# Reload after editing /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure
```

#### WPA-PSK
* https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access#Target_users_.28authentication_key_distribution.29
    * Generate key using Python
      ```python
      import hashlib, binascii
      binascii.hexlify(hashlib.pbkdf2_hmac("sha1", str.encode("password"), str.encode("ssid"), 4096, 32))
      ``` 
    * https://stackoverflow.com/questions/46502224/python-wpa-passphrase-linux-binary-implementation-generates-only-part-of-the-p/62758303#62758303
    * WPA PSK (Raw Key) Generator: https://www.wireshark.org/tools/wpa-psk.html

#### Netplan
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

### Policy-Based Routing (PBR)

#### Two IPs with different default gateways (depending on connection source address)

`/etc/iproute2/rt_tables`
```
#
# reserved values
#
255	local
254	main
253	default
0	unspec
#
# local
#
#1	inr.ruhep

100 net_0
101 net_20
```

`/etc/network/interfaces`
```
auto ens160

iface ens160 inet static
address 10.20.1.111
netmask 255.255.254.0
gateway 10.20.1.1

iface ens160 inet static
address 10.0.1.111
netmask 255.255.254.0

post-up ip rule add prio 100 from 10.0.1.0/23 lookup net_0
post-up ip route add 0.0.0.0/0 via 10.0.1.1 table net_0
post-up ip rule add prio 100 from 10.20.1.0/23 lookup net_20
post-up ip route add 0.0.0.0/0 via 10.20.1.1 table net_20

post-down ip rule del prio 100 from 10.0.1.0/23 lookup net_0 || true
post-down ip route del 0.0.0.0/0 via 10.0.1.1 table net_0 || true
post-down ip rule del prio 100 from 10.20.1.0/23 lookup net_20 || true
post-down ip route del 0.0.0.0/0 via 10.20.1.1 table net_20 || true
```

* https://www.mybluelinux.com/debian-source-routing/
* Research path for netplan
    * `routing-policy`
    * https://netplan.io/reference/
    * https://www.paranoids.at/ubuntu-18-04-netplan-source-routing/
