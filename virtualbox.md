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

