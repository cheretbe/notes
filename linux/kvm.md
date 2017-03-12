* Ubuntu. Package to enter password for remote connections over SHH: `ssh-askpass`
* https://sebastian.marsching.com/wiki/Linux/KVM

### Guest Settings
Windows Virtio drivers: https://fedoraproject.org/wiki/Windows_Virtio_Drivers#Direct_download

Enable policy: Local Computer Policy > Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options `"Shutdown: Allow system to be shut down without having to log on"` 
```batch
:: Query current policy setting
reg.exe QUERY "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v shutdownwithoutlogon
If it is 0x0, update to 0x1
reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v shutdownwithoutlogon /t REG_DWORD /d 0x1 /f
```

Shutdown timeout
```batch
:: Query current ShutdownWarningDialogTimeout value
reg.exe QUERY "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" /v ShutdownWarningDialogTimeout
:: If it is 0xffffffff, update to 0x00000001
reg.exe ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows" /v ShutdownWarningDialogTimeout /t REG_DWORD /d 0x1 /f
```

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
  # [!!!] Make sure bridge-utils package is installed
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
###Copying a VM
Copy the VM's disks from `/var/lib/libvirt/images` on src host to the same dir on destination host
```shell
# on the source host run
virsh dumpxml VMNAME > domxml.xml
# and copy this xml to the dest. host
# on the destination host run
virsh define domxml.xml
```
Start new VM.
If the disk location differs, you need to edit the xml's devices/disk node to point to the image on the destination host. If the VM is attached to custom defined networks, you'll need to either edit them out of the xml on the destination host or redefine them as well
```shell
virsh net-dumpxml > netxml.xml
# and
virsh net-define netxml.xml && virsh net-start NETNAME & virsh net-autostart NETNAME
```
To edit existing (registered) vm:
```shell
export EDITOR=nano
virsh edit vmname
```
VM's configs are in `/etc/libvirt/qemu`
* http://serverfault.com/questions/434064/correct-way-to-move-kvm-vm
