* Speed/storage converters:
    * https://wintelguy.com/filesizeconv.pl
    * https://www.gbmb.org/
* SHA1 sums: https://www.heidoc.net/php/myvsdump_directory.php?letter=W

#### Linux

Nano: https://github.com/cheretbe/notes/blob/master/linux/nano.md

```shell
# view setting
vboxmanage list systemproperties | grep "Default machine folder:"
# SSD
vboxmanage setproperty machinefolder /home/GUR/2301/vm/
# HDD
vboxmanage setproperty machinefolder /mnt/vmdata/vm/

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@host.tld

# Write speed test
# 20GiB, 1KiB block: bs=1k count=$((20*1024*1024))
# 20GiB, 1MiB block:
sync; dd if=/dev/zero of=tempfile bs=1M count=$((20*1024)) status=progress; sync
# Read speed test
#~~vm.drop_caches = 3~~
echo 3 | sudo tee /proc/sys/vm/drop_caches 
dd if=tempfile of=/dev/null bs=1M count=$((10*1024)) status=progress

tar czvf file.tar.gz directory/

ps aux | grep python
```
#### Windows

Ctrl+Alt+Del menu in RDP client: <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>End</kbd>

```powershell
# Set network location to private
Get-NetConnectionProfile
Set-NetConnectionProfile -InterfaceIndex 13 -NetworkCategory Private

# View motherboard name
Get-WmiObject Win32_BaseBoard | Select-Object Manufacturer, Product

# Search services by display name
Get-Service | Where-Object { $_.DisplayName -like "*media*" }
# Get details by name
Get-Service WMPNetworkSvc
```
```batch
:: start= <boot|system|auto|demand|disabled|delayed-auto>
sc.exe config WinRM start= auto
sc.exe start WinRM
```
| Service       | English Name                                 | Russian Name                                              |
| ------------- | -------------------------------------------- | --------------------------------------------------------- |
| WMPNetworkSvc | Windows Media Player Network Sharing Service | Служба общих сетевых ресурсов проигрывателя Windows Media |
| wuauserv      | Windows Update                               | Центр обновления Windows                                  |
