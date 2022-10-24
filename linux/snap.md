* https://askubuntu.com/questions/1412575/pending-update-of-snap-store/1412580#1412580
```shell
# Close all Chromium windows (without doing this snap refresh shows "helpful" message: All snaps up to date)
sudo snap refresh
```

```shell
# By default, snaps are set to refresh themselves 4 times per day
sudo snap set system refresh.timer=sat,04:00

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
