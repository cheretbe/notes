###Installation
To check if hardware acceleration is enabled install package `cpu-checker` and run `kvm-ok` as root. KVM is basically a hardware-accelerated version of QEMU
``` bash
apt update
apt install bridge-utils qemu-kvm virt-manager
# Add a user to kvm and libvirtd groups (logoff/logon to take effect)
adduser username kvm
adduser username libvirtd
```
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
