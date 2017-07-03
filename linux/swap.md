* https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04
* http://askubuntu.com/questions/33697/how-do-i-add-a-swap-partition-after-system-installation/33703#33703

```shell
# Identify configured swap devices and files
cat /proc/swaps

# Disable swap device
swapoff /dev/sda5

# Turn off all swap devices
swapoff -a
```

#### Swappines
Add to `/etc/sysctl.conf`:
```
vm.swappiness = 1
```
```shell
# Apply changes without a reboot
sysctl vm.swappiness=1
# Check current setting
cat /proc/sys/vm/swappiness
```
