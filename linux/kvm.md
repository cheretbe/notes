Installation (To check if hardware acceleration is enabled install package `cpu-checker` and run `kvm-ok` as root)
``` bash
apt update
apt install bridge-utils qemu-kvm virt-manager
# Add a user to kvm and libvirtd groups (logoff/logon to take effect)
adduser username kvm
adduser username libvirtd
