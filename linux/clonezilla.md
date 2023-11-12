* https://github.com/stevenshiau/clonezilla
* https://github.com/stevenshiau/drbl

Network config
```shell
# Find out physical WiFi device name
iw dev

# Connect to a hidden WiFi network
ocs-live-netcfg
# or just run nmtui directly
# 1. Use "Edit a connection" menu in NetworkManager TUI to add a connection (or 
# 2. Activate it manually
nmcli con up HIDDEN_WIFI_PROFILE_NAME
```

Change device names
```shell
# View current device names
# nvme0n1 nvme1n1
cat 2021-03-28-05-img/disk

# Change to scd and sdd
cnvt-ocs-dev 2021-03-28-05-img nvme0n1 sdc
cnvt-ocs-dev 2021-03-28-05-img nvme1n1 sdd
```

```shell
# Run TUI over SSH (/usr/sbin/clonezilla)
# [!!!] Use screen utility
clonezilla
```

When cloning remotely to a smaller disk `-icds` option on source doesn't work (and TUI menu
on destination doesn't offer advanced settings). To solve this problem run `ocs-onlthefly` manually.<br>
:bulb: Also on a source use expert mode to enable `cat` (no compression) instead of default `gz` for slow machines. For fast multicore machines
also use expert mode and select `gz` (seems to enable `pigz` usage as opposed to default). 
```shell
# [!] Source listens on ports 9000-9006

# on destination
# [!] timeout option is useful on systems with multiple network cards (default is 30s per adapter)
ocs-live-netcfg -t 5
ocs-onthefly [--net-filter cat] -s 192.168.1.1 -d /dev/sdX [-icds]
```
