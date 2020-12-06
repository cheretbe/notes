### Local cache

* apt-cacher-ng
    * https://wiki.debian.org/AptCacherNg
    * **https://kifarunix.com/how-to-setup-apt-caching-server-using-apt-cacher-ng-on-ubuntu-18-04/**
    * http://vasilisc.com/apt-cacher-ng
* squid-deb-proxy (for a dev machine)
    * https://tribaal.io/making-lxd-fly-on-ubuntu-as-well.html

```shell
apt install apt-cacher-ng
```
Config is in `/etc/apt-cacher-ng/acng.conf`

Default cache location is `/var/cache/apt-cacher-ng` (`CacheDir` parameter). When the value for
`CacheDir` is changed, update `RequiresMountsFor` in the `/lib/systemd/system/apt-cacher-ng.service`
file too.

```shell
mkdir /package-cache/apt-cacher
chown apt-cacher-ng:apt-cacher-ng /package-cache/apt-cacher

nano /etc/apt-cacher-ng/acng.conf
nano /lib/systemd/system/apt-cacher-ng.service

systemctl daemon-reload
# Directory structure is created on start
service apt-cacher-ng restart
```

view status at `http://host.domain.tld:3142/`, (select `Statistics report and configuration page` in `Related links`)

```shell
cat <<EOF >/etc/apt/apt.conf.d/02proxy
  Acquire::http::proxy "http://host.domain.tld:3142";
  Acquire::ftp::proxy "http://host.domain.tld:3142";
EOF
```

### Unsorted

* Package `distro-info-data` contains distribution release info (`/usr/share/distro-info/debian.csv`, `/usr/share/distro-info/ubuntu.csv`)

```shell
# Disable weekly LTS upgrade notification
# Edit /etc/update-manager/release-upgrades
# And replace 'Prompt=lts' with 'Prompt=never'
cat /etc/update-manager/release-upgrades
sed -i 's/^Prompt.*/Prompt=never/' /etc/update-manager/release-upgrades

# Kill background unattended upgrades script that prevents apt from running
# (repeat a couple of times)
lsof /var/lib/dpkg/lock-frontend | awk 'NR > 1 {print $2}' | xargs -p --no-run-if-empty kill

# Enable the 'universe' repository
add-apt-repository universe

# View the list of configured repos and PPAs
apt-cache policy

# View the list of packages provided by a repository
apt update
ls /var/lib/apt/lists/*_Packages
# Find out repo name, e.g. "repo.zabbix.com_zabbix_"
grep ^Package /var/lib/apt/lists/repository-name*_Packages | awk '{print $2}' | sort -u

# Remove a PPA
sudo add-apt-repository -r ppa:colingille/freshlight
# Fix missing dependencies
apt-get -f -y install

# Install 32-bit version of a package on a 64-bit OS
apt install libncursesw5:i386

# Find out which package provides a file
# (apt-file also could be used, but it is not installed by default and see notes below on list files size)
dpkg -S libstdc++.so.6

# Download package file to current directory (doesn't require root privileges)
# When run as root just ignore "Download is performed unsandboxed as root as file etc..." warning
apt download package
apt-get download package

# List files, that were installed by a package
dpkg -L package

# List files, that WILL be installed by a package BEFORE installing it
# Note on apt-file disk usage:
# It installs /etc/apt/apt.conf.d/50apt-file.conf file, that contains settings
# to download Contents files on update. Due to these settings the size of
# /var/lib/apt/lists/ directory increases significantly. Purging apt-file package
# and updating list of packages reduces it back
apt install apt-file
apt update
apt-file list package

# List DEB package contents
dpkg --contents package.deb

# Extract DEB package conents without installing
# [!] Directory to extract is NOT optional. Will be created if doesn't exist
dpkg-deb -xv package.deb /path/to/extract

# Downgrade a package
# Check currently installed version
dpkg -l firefox
# View available versions
apt-cache policy firefox
# or
apt-cache showpkg firefox
# Downgrade
apt-get install firefox=45.0.2+build1-0ubuntu1
# Hold the downgraded version
apt-mark hold firefox
# Unhold
apt-mark unhold firefox
# List held packages
apt-mark showhold
# or
dpkg -l | grep "^hi"
```

dpkg options are in `/etc/dpkg/dpkg.cfg.d` (for example, Docker container may have some
`path-exclude` settings in `/etc/dpkg/dpkg.cfg.d/excludes`)

* apt-listchanges: http://jxf.me/entries/better-apt-ubuntu/

Programmatically check if a package is not installed
```bash
# -W|--show [<pattern> ...] Show information on package(s)
# -f changes the format of the output
# db:Status-abbrev contains the abbreviated package status (as three characters),
#   such as "ii " or "iHR" (since dpkg 1.16.2) See the --list command example below
#   for more details.

# So here we are checking for presence of "i" at position 2 of three-char output
if ! dpkg-query -Wf'${db:Status-abbrev}' "htop" 2>/dev/null | grep -q '^.i'; then
  echo "htop is not installed"
fi
```
Tools like aptitude can mark some packages for removal, some for purge and some others for install,
downgrade, etc. Then with a single command do all necessary stuff to trigger pending actions. The
desired field is used to determine what should be done with a package.
```
dpkg-query -l htop
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                      Version           Architecture      Description
+++-=========================-=================-=================-========================================================
ii  htop                      2.1.0-3           amd64             interactive processes viewer
```

Local apt mirror
* https://computingforgeeks.com/creating-ubuntu-mirrors-using-apt-mirror/
* https://linuxconfig.org/how-to-create-a-ubuntu-repository-server
