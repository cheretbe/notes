```shell
# View (in human-readable form) if the package is installed
dpkg-query -l snapd

# Completely remove snapd
# https://askubuntu.com/questions/1345385/how-can-i-stop-apt-from-installing-snap-packages/1345401#1345401

sudo apt autoremove --purge snapd

# Prevent snapd installation in the future
cat <<EOF | sudo tee /etc/apt/preferences.d/nosnap.pref
# To prevent repository packages from triggering the installation of Snap,
# this file forbids snapd from being installed by APT.
# For more information: https://linuxmint-user-guide.readthedocs.io/en/latest/snap.html

Package: snapd
Pin: release a=*
Pin-Priority: -10
EOF
```


* https://askubuntu.com/questions/1412575/pending-update-of-snap-store/1412580#1412580
```shell
# Close all Chromium windows (without doing this snap refresh shows "helpful" message: All snaps up to date)
sudo snap refresh
```

```shell
# By default, snaps are set to refresh themselves 4 times per day
sudo snap set system refresh.timer=sat,04:00

sudo snap connections remmina

sudo snap connect remmina:audio-record :audio-record
sudo snap connect remmina:avahi-observe :avahi-observe
sudo snap connect remmina:cups-control :cups-control
sudo snap connect remmina:mount-observe :mount-observe
sudo snap connect remmina:password-manager-service :password-manager-service
sudo snap connect remmina:ssh-keys :ssh-keys
sudo snap connect remmina:ssh-public-keys :ssh-public-keys
# Then change where Remmina profiles are stored using preferences

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
