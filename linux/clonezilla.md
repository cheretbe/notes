```shell
# Run TUI over SSH (/usr/sbin/clonezilla)
clonezilla
```

When cloning remotely to a smaller disk `-icds` option on source doesn't work (and TUI menu
on destination doesn't offer advanced settings). To solve this problem run `ocs-onlthefly` manually.<br>
:bulb: Also on a source use expert mode to enable `cat` (no compression) instead of default `gz` for slow machines. For fast multicore machines
also use expert mode and select `gz` (seems to enable `pigz` usage as oppozed to default). 
```shell
# on destination
# [!] timeout option is useful on systems with multiple network cards (default is 30s per adapter)
ocs-live-netcfg -t 5
ocs-onthefly [--net-filter cat] -s 192.168.1.1 -d /dev/sdX [-icds]
```
