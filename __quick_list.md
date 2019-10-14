* Speed/storage converters:
    * https://wintelguy.com/filesizeconv.pl
    * https://www.gbmb.org/
* SHA1 sums: https://www.heidoc.net/php/myvsdump_directory.php?letter=W

#### Linux

Nano: https://github.com/cheretbe/notes/blob/master/linux/nano.md

```shell
# Reboot today at 23:00
at $(date +"23:00 %Y-%m-%d") <<EOF
echo "\$(date) - Rebooting $(hostname -f)" \
   | mail $USER -s "Scheduled reboot of $(hostname -f)"
/sbin/reboot
EOF
```

```shell
# Download torrent
cd ~/Downloads
aria2c --seed-time 0 http://releases.ubuntu.com/16.04/ubuntu-16.04.3-server-amd64.iso.torrent
# Magnet link
aria2c --enable-dht=true --seed-time 0 "magnet:?xt=urn:btih:2D..."


# Kill background unattended upgrades script
# (repeat a couple of times)
lsof /var/lib/dpkg/lock-frontend | awk 'NR > 1 {print $2}' | xargs -p --no-run-if-empty kill

# Continuously updated iostat
watch -n 1 iostat -xy --human 1 1

# view setting
vboxmanage list systemproperties | grep "Default machine folder:"
# SSD
vboxmanage setproperty machinefolder /home/GUR/2301/vm/
# HDD
vboxmanage setproperty machinefolder /mnt/vmdata/vm/

# check mail delivery ('mailutils' package needs to be installed)
echo test | mail -s "test mail" root

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=5 -o ServerAliveCountMax=2 user@host.tld
ssh-copy-id -i ~/.ssh/key_name.pub user@host.tld

# Find file recursively
# -iname:  like -name, but the match is case insensitive
find / -xdev -iname "*sql*"

# Grep the whole filesystem
# -xdev  Don't descend directories on other filesystems.
# -H, --with-filename  print the file name for each match
# -I  equivalent to --binary-files=without-match
find / -xdev -type f -print0 | xargs -0 grep -H -I "ForceCompositionPipeline"
# -m 1 to return only the first match

# Write speed test
# 20GiB, 1KiB block: bs=1k count=$((20*1024*1024))
# 20GiB, 1MiB block:
sync; dd if=/dev/zero of=tempfile bs=1M count=$((20*1024)) status=progress; sync
# Read speed test
#~~vm.drop_caches = 3~~
echo 3 | sudo tee /proc/sys/vm/drop_caches 
dd if=tempfile of=/dev/null bs=1M count=$((20*1024)) status=progress

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
powershell "Get-Service | Where-Object { $_.DisplayName -like '*registry*' }"
powershell "Get-Service | Where-Object { $_.Name -like '*remote*' }"
:: System.ServiceProcess.ServiceController does not containg PathName, so it
:: is necessary to use WMI
powershell "Get-WmiObject win32_service | Where-Object {$_.PathName -like '*exename*'} | Select Name, DisplayName, State, PathName"
:: start= <boot|system|auto|demand|disabled|delayed-auto>
sc.exe config WinRM start= auto
sc.exe start WinRM
```
| Service        | English Name                                 | Russian Name                                              |
| -------------- | -------------------------------------------- | --------------------------------------------------------- |
| WMPNetworkSvc  | Windows Media Player Network Sharing Service | Служба общих сетевых ресурсов проигрывателя Windows Media |
| wuauserv       | Windows Update                               | Центр обновления Windows                                  |
| RemoteRegistry | Remote Registry                              | Удаленный реестр                                          |
