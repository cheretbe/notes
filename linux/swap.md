https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04

http://askubuntu.com/questions/33697/how-do-i-add-a-swap-partition-after-system-installation/33703#33703

#### Swappines
Add to `/etc/sysctl.conf`:
```
vm.swappiness = 0
```
```shell
# Apply changes without a reboot
sysctl vm.swappiness=0
# Check current setting
cat /proc/sys/vm/swappiness
```
