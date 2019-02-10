```shell
# View the list of configured repos and PPAs
apt-cache policy
# Remove a PPA
sudo add-apt-repository -r ppa:colingille/freshlight
# Fix missing dependencies
apt-get -f -y install

# Install 32-bit version of a package on a 64-bit OS
apt install libncursesw5:i386

# Find out which package provides a file
# (apt-file also could be used, but it is not installed by default and seem to use its own cache)
dpkg -S libstdc++.so.6

# Downgrade a package
# Check currently installed version
dpkg -l firefox
# View available versions
apt-cache showpkg firefox
# or
apt-cache policy firefox
# Downgrade
apt-get install firefox=45.0.2+build1-0ubuntu1
# Hold the downgraded version
apt-mark hold firefox
# Unhold
apt-mark unhold firefox
```

* apt-listchanges: http://jxf.me/entries/better-apt-ubuntu/
