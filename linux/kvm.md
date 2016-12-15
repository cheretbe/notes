###Installation
To check if hardware acceleration is enabled install package `cpu-checker` and run `kvm-ok` as root. KVM is basically a hardware-accelerated version of QEMU
``` bash
apt update
apt install bridge-utils qemu-kvm virt-manager
# Add a user to kvm and libvirtd groups (logoff/logon to take effect)
adduser username kvm
adduser username libvirtd
# https://bugs.launchpad.net/ubuntu/+source/virt-manager/+bug/1550983
# If virt-manager fails to start with error message "Couldn't open libGL.so.1: libGL.so.1:
# cannot open shared object file: No such file or directory"
apt install libgl1-mesa-glx
```
###Networking
Add bridged network adapter to `/etc/network/interfaces`
```
auto eth0
iface eth0 inet manual

auto br0
iface br0 inet static
  address 192.168.1.2
  netmask 255.255.255.0
  #network 192.168.1.0
  #broadcast 192.168.1.255
  gateway 192.168.1.1
  dns-nameservers 192.168.1.1
  dns-search home.local
  bridge_ports eth0
  bridge_fd 0
  bridge_hello 2
  brigge_maxage 12
  #bridge_stp off
```
Some info on bridge parameters:
* http://manpages.ubuntu.com/manpages/xenial/man5/bridge-utils-interfaces.5.html
* http://manpages.ubuntu.com/manpages/xenial/en/man8/brctl.8.html

VLAN
```bash
apt install vlan
# Load kernel module
modprobe 8021q
# Add VLAN with id 100 to eth0
vconfig add eth0 100
# Assign an address to the new interface
ip addr add 10.0.0.1/24 dev eth0.100

# Make this setup permanent
echo "8021q" >> /etc/modules
# /etc/network/interfaces
# auto eth0.100
# iface eth0.100 inet dhcp
#   vlan-raw-device eth0
```
