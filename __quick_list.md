```shell
# view setting
vboxmanage list systemproperties | grep "Default machine folder:"
# SSD
vboxmanage setproperty machinefolder /home/GUR/2301/vm/
# HDD
vboxmanage setproperty machinefolder /mnt/vmdata/vm/
```
