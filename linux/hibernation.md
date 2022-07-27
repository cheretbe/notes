```shell
swapoff /swapfile
# Create swap file at least as large as the computer's RAM
dd if=/dev/zero of=/swapfile bs=$(cat /proc/meminfo | awk '/MemTotal/ {print $2}') count=1024 conv=notrunc
mkswap /swapfile
swapon /swapfile
```
