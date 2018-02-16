#### Linux

Nano: https://github.com/cheretbe/notes/blob/master/linux/nano.md

```shell
# view setting
vboxmanage list systemproperties | grep "Default machine folder:"
# SSD
vboxmanage setproperty machinefolder /home/GUR/2301/vm/
# HDD
vboxmanage setproperty machinefolder /mnt/vmdata/vm/

ssh user@host.tld -o "UserKnownHostsFile /dev/null"

# Write speed test
sync; dd if=/dev/zero of=tempfile bs=1M count=1024 status=progress; sync
# Read speed test
vm.drop_caches = 3
dd if=tempfile of=/dev/null bs=1M count=1024 status=progress
```
#### Windows

Ctrl+Alt+Del menu in RDP client: <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>End</kbd>

```powershell
# View motherboard name
Get-WmiObject Win32_BaseBoard | Select-Object Manufacturer, Product
```
