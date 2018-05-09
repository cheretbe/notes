* Speed/storage converter: https://www.gbmb.org/

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
#~~vm.drop_caches = 3~~
echo 3 | sudo tee /proc/sys/vm/drop_caches 
dd if=tempfile of=/dev/null bs=1M count=1024 status=progress

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
