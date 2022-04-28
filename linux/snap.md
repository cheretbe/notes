```shell
sudo snap connections remmina

snap changes

# install specific version of a package
snap install go --channel=1.15/stable --classic
# list available versions
snap info go
# update to the latest version
snap refresh --channel=latest/stable go

# snap refresh only installs those specific versions offered in snap info
# But by default, it keeps two previous versions of every package cached
# revert latest update
snap revert go
```
