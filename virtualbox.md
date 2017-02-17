To be able to add USB devices on **host** in Linux:
```
sudo adduser <npa> vboxusers
```

### Shared Folders Write Access in Linux
Access to auto-mounted shared folders is only granted to the user group vboxsf, which is created by the VirtualBox Guest Additions installer. Hence guest users have to be member of that group to have read/write access or to have read-only access in case the folder is not mapped writable.
```shell
sudo adduser <username> vboxsf
# or
usermod -a -G vboxsf <username>
```
### Compacting VDI
#### Linux
The most simple way is to boot from Live CD (to avoid remounting `/` as readonly)
```shell
# Install zerofree (enable universe)
add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
apt-get update
apt-get install zerofree
# Clear root
zerofree –v /dev/sda1
# Clear the swap space, assuming it is /dev/sda5
swapoff /dev/sda5
blkid /dev/sda5 -s UUID -o value > uuid.tmp
dd if=/dev/zero of=/dev/sda5 bs=1M
mkswap /dev/sda5
swaplabel -U $(cat uuid.tmp) /dev/sda5
```
In the host
```
 VBoxManage modifyhd --compact <disk_name>.vdi
```


### Create dynamic VDI
```
VBoxManage createhd --filename <path to your vdi> --size <size in megabytes>
```
* 15Gb – 15360
* 20Gb – 20480
* 25Gb – 25600
* 30Gb – 30720

### Virtual disks identification
```shell
# IDE
VBoxManage setextradata "VMName" "VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/SerialNumber" "091118FC1221NCJ6G8GG"
VBoxManage setextradata "VMName" "VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/FirmwareRevision" "FC2ZF50B"
VBoxManage setextradata "VMName" "VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/ModelNumber" "HITACHI HTD723216L9SA60"
# SATA
VBoxManage setextradata "VMname" "VBoxInternal/Devices/ahci/0/Config/Port0/SerialNumber" "serial"
VBoxManage setextradata "VMname" "VBoxInternal/Devices/ahci/0/Config/Port0/FirmwareRevision" "firmware"
VBoxManage setextradata "VMname" "VBoxInternal/Devices/ahci/0/Config/Port0/ModelNumber" "model"
```
In the client
```shell
# Linux
lshw -class disk
```

