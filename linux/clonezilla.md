When cloning remotely to a smaller disk `-icds` option on source doesn't work (and TUI menu
on destination doesn't offer advanced settings). To solve this problem run `ocs-onlthefly` manually
```shell
# on destination
ocs-onthefly -s 192.168.1.1 -t sda -icds
```
