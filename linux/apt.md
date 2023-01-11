```shell
# [!!!]
apt-cache search openjdk
apt-cache policy openjdk-18-jre

# Verbose output
sudo apt -oDebug::pkgAcquire::Worker=1 update

# TODO: try to use .asc if a key needs unpacking
#   https://stackoverflow.com/questions/71585303/how-can-i-manage-keyring-files-in-trusted-gpg-d-with-ansible-playbook-since-apt#comment129873032_72548342
#   https://stackoverflow.com/questions/71585303/how-can-i-manage-keyring-files-in-trusted-gpg-d-with-ansible-playbook-since-apt/73805885#73805885
# --dearmor    Pack or unpack an arbitrary input into/from an OpenPGP ASCII armor
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant

apt-key list
# CDFFDE29 (last 4 bytes) could also be used
apt-key export 'D563 11E5 FF3B 6F39 D5A1  6ABE 18DF 3741 CDFF DE29' | gpg --dearmor | sudo tee /usr/share/keyrings/anydesk-keyring.gpg
# deb [signed-by=/usr/share/keyrings/anydesk-keyring.gpg] http://deb.anydesk.com/ all main
```

### Change mirror

```shell
# https://askubuntu.com/questions/39922/how-do-you-select-the-fastest-mirror-from-the-command-line/719551#719551
# [!] Here we changing the range from 100KiB (102400 bytes) to 1MiB (1048576 bytes)
# Use the original value for scripts to speed up testing process
curl -s http://mirrors.ubuntu.com/mirrors.txt | xargs -n1 -I {} sh -c 'echo `curl -r 0-1048576 -s -w %{speed_download} -o /dev/null {}/ls-lR.gz` {}' | sort -g -r | head -1 | awk '{ print $2 }'

cp /etc/apt/sources.list{,.bak}
# Assuming that testing result is http://archive.ubuntu.com/ubuntu
sed -i 's#http://archive.ubuntu.com/ubuntu#http://mirror.corbina.net/ubuntu#' /etc/apt/sources.list
```

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
Config is in `/etc/apt-cacher-ng/acng.conf` (:warning: debconf parameters are in `/etc/apt-cacher-ng/zz_debconf.conf` - WTF?)

Default cache location is `/var/cache/apt-cacher-ng` (`CacheDir` parameter). When the value for
`CacheDir` is changed, update `RequiresMountsFor` in the `/lib/systemd/system/apt-cacher-ng.service`
file too (:warning: Use `systemctl edit apt-cacher-ng.service` to create drop-in file).

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

### Debconf configuration preseeding

```shell
# debconf-utils has to be installed
apt install debconf-utils

# Use 'debconf-show package' or 'debconf-get-selections | grep package' to view
# all available questions (package has to be installed)
# To view text descriptions and choices open full selection DB dump and use search
debconf-get-selections | less

echo "get postfix/main_mailer_type" | debconf-communicate
echo "set postfix/main_mailer_type 'Internet with smarthost'" | debconf-communicate
```
Check what this does
```shell
apt-get clean
cat >> /etc/apt/apt.conf <<EOF
// Pre-configure all packages before
// they are installed.
DPkg::Pre-Install-Pkgs {
    "dpkg-preconfigure --apt --priority=low";
};
EOF
apt-get upgrade
```

Ansible
```yaml
- name: Configure APT apt-cache-ng package (Allow HTTP tunnels through Apt-Cacher NG)
  debconf:
    name: apt-cache-ng
    question: "apt-cacher-ng/tunnelenable"
    value: "true" # value is string
    vtype: boolean
    
- name: Configure APT postfix package (internet with smarthost)
  debconf:
    name: postfix
    question: "postfix/main_mailer_type"
    value: "Internet with smarthost"
    vtype: select
```

### Unsorted

* Package `distro-info-data` contains distribution release info (`/usr/share/distro-info/debian.csv`, `/usr/share/distro-info/ubuntu.csv`)

```shell
# if dpkg-reconfigure doesn't show dialogs check DEBIAN_FRONTEND variable value
# and make sure 'dialog' package is installed
echo $DEBIAN_FRONTEND
apt install dialog
DEBIAN_FRONTEND=dialog dpkg-reconfigure tzdata

# Temporarily change the minimum priority of question debconf will display
DEBIAN_PRIORITY=low apt install postfix

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
# Use -R to extract control info too
dpkg-deb -Rv package.deb /path/to/extract

# Restore original versions of modified and deleted files
# First find out which package installed the file (in this example it's systemd)
dpkg -S /etc/systemd/resolved.conf
# [!!!!!] Thread carefully, as this will overwrite configs without asking (and -s
#         option doesn't show what's going to be done)
apt install --reinstall -o Dpkg::Options::="--force-confask,confnew,confmiss" systemd

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

Programmatically downgrade a package
```bash
if [[ $(dpkg-query -W -f='${Version}' virtualbox-guest-utils) = "6.1.22-dfsg-2~ubuntu1.20.04.1" ]]; then
  echo "Downgrading 'virtualbox-guest-utils' package"
  /usr/bin/sudo -n -- sh -c "DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --allow-downgrades virtualbox-guest-utils=6.1.16-dfsg-6~ubuntu1.20.04.2"
  /usr/bin/sudo -n -- sh -c "DEBIAN_FRONTEND=noninteractive apt-mark hold virtualbox-guest-utils"
fi
```

Local apt mirror
* https://computingforgeeks.com/creating-ubuntu-mirrors-using-apt-mirror/
* https://linuxconfig.org/how-to-create-a-ubuntu-repository-server
