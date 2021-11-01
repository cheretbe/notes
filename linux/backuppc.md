* http://backuppc.sourceforge.net/
* https://github.com/backuppc/backuppc
* https://sourceforge.net/p/backuppc/mailman/
* https://github.com/backuppc/backuppc/wiki/Installing-BackupPC-4-from-tarball-or-git-on-Ubuntu
* https://serverfault.com/questions/662027/backuppc-schedule-advanced-settings/662150#662150
* https://gogs.zionetrix.net/bn8/check_backuppc
* Review:
    * https://sourceforge.net/p/backuppc/mailman/message/33596562/
    * http://www.guyrutenberg.com/2014/01/14/restricting-ssh-access-to-rsync/
    * :warning: test rsync's --filter option: https://sourceforge.net/p/backuppc/mailman/backuppc-users/thread/20071106234318.GR9017%40renesys.com/
* Config parsing
    * https://github.com/evs38/zabbix-agent-addons/blob/master/zabbix_scripts/disco_backuppc_sudo
    * https://github.com/backuppc/backuppc/blob/master/lib/BackupPC/CGI/EditConfig.pm


:warning: For SMB and tar, BackupPC uses the modification time (mtime) to determine which files have changed since the last backup. That means SMB and tar incrementals **are not able to detect** deleted files, renamed files or new files whose modification time is prior to the last lower-level backup.
* https://backuppc.github.io/backuppc/BackupPC.html#Backup-basics

### Config

- [ ] 1. Generate `/var/lib/backuppc/.ssh/id_rsa` and `/var/lib/backuppc/.ssh/id_rsa.pub`
```shell
# As user backuppc-server
pwd
ssh-keygen -C "BackupPC key"
```
----------
- [ ] 2. Edit global config  

[$Conf{FullKeepCnt}](https://backuppc.github.io/backuppc/BackupPC.html#_conf_fullkeepcnt_): `1*$Conf{FillCycle}`, `2*$Conf{FillCycle}`, `4*$Conf{FillCycle}`, `8*$Conf{FillCycle}`, etc.<br>
If `$Conf{FillCycle}` is `0`, then `$Conf{FullPeriod}` is used instead.<br>
With defaults `$Conf{FillCycle} = 0;` and `$Conf{FullPeriod} = 6.97;` this gives us the following exponential sequence:<br>
`1 week, 2 weeks, 1 month, 2 months, 4 months, 8 months, etc.`
```
With $Conf{FullKeepCnt} = [4, 6, 12, 12, 5];
--------------+---------------------
4 x 1 week    | 1 month
6 x 2 weeks   | 3 months
12 x 1 month  | 12 months
12 x 2 months | 24 months
5 x 4 months  | 20 months
--------------+---------------------
total         | 60 months = 5 years
--------------+---------------------

With $Conf{FullKeepCnt} = [4, 6, 12, 12];
40 months ~ 3.3 years
```
```perl
# Turn off compression when using ZFS dataset with compression
$Conf{CompressLevel} = 0;

$Conf{FullKeepCnt} = [4, 6, 12, 12, 5];
# 1870 days ~ 5.1 years
$Conf{FullAgeMax} = 1870;

# or
$Conf{FullKeepCnt} = [4, 6, 12, 12];
# 1240 days ~ 3.39 years
$Conf{FullAgeMax} = 1240;

$Conf{IncrKeepCnt} = 30;
$Conf{IncrAgeMax} = 60;

# String for copypasting
# 1, 2, 3, 4, 5, 6, 7, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 18, 19, 20, 21, 22, 23
$Conf{WakeupSchedule} = [1, 2, 3, 4, 5, 6, 7, 8, '8.5', 9, '9.5', 10, '10.5', 11, '11.5', 12, '12.5', 13, '13.5', 14, '14.5', 15, '15.5', 16, '16.5', 17, 18, 19, 20, 21, 22, 23];
$Conf{EMailAdminUserName} = 'backuppc-server'
# Apache2 http users
# [!!!!] When using Ansigle config, double check that there are no duplicate entries at the end of the file
$Conf{CgiAdminUsers} = 'user1 user2';
```
----------
- [ ] 3. Add localhost. `localhost.pl` example:
```perl
$Conf{BackupFilesExclude} = {
  '/home' => [
    '/*/temp'
  ],
  '/root' => [
    '/temp'
  ],
  '/share/subdir' => [
    '/temp'
  ]
};
$Conf{RsyncShareName} = [
  '/etc',
  '/home',
  '/root',
  '/usr/local',
  '/share/subdir'
];
$Conf{XferMethod} = 'rsync';
$Conf{RsyncClientPath} = 'nice -n 19 sudo /usr/bin/rsync';
$Conf{RsyncSshArgs} = [
  '-e',
  '$sshPath -l backuppc'
];
$Conf{BackupPCNightlyPeriod} = 1;
```

:warning: Don't copy/paste this code directly, use [edit_as_utf8.py](https://github.com/cheretbe/backuppc-scripts/blob/master/util/edit_as_utf8.py) script<br>
:warning: Note double qoutes on non-iso-8859-1 strings
* Typical Windows exclusions
    * (:warning:**TODO:** change link to master branch after release) [typical_windows_exclusions.txt](https://github.com/cheretbe/backuppc-scripts/blob/develop/tools/typical_windows_exclusions.txt)
    * Direct download link: https://raw.githubusercontent.com/cheretbe/backuppc-scripts/develop/tools/typical_windows_exclusions.txt
    * ❓add `/Users/*/AppData/Local/Packages`

### Installation
Only for new installation, skip this for upgrade
```shell
# 20.04
apt install apache2 apache2-utils libapache2-mod-perl2 smbclient \
  rrdtool libarchive-zip-perl libfile-listing-perl \
  libxml-rss-perl libcgi-session-perl make gcc par2 \
  libacl1 libacl1-dev

apt-get install apache2 apache2-utils libapache2-mod-perl2 smbclient rrdtool libapache2-mod-scgi \
    libarchive-zip-perl libfile-listing-perl libxml-rss-perl libcgi-session-perl make gcc par2 \
    libacl1 libacl1-dev
    
# Check if sendmail is installed (note the trailing '*')
dpkg -l sendmail*
# Remove it if installed
apt purge sendmail*
# Install and configure postfix
apt install postfix
dpkg-reconfigure postfix --priority low

adduser --system --home /var/lib/backuppc --group --disabled-password --shell /bin/false backuppc-server

rmdir /var/lib/backuppc/
mkdir /path/to/backup/dir
chown backuppc-server:backuppc-server /path/to/backup/dir
ln -s /path/to/backup/dir /var/lib/backuppc

mkdir -p /var/lib/backuppc/.ssh
chmod 700 /var/lib/backuppc/.ssh
# [!] 'StrictHostKeyChecking no' parameter is optional, it allows connecting to any host
# without explicityly adding it to .ssh/known_hosts
echo -e "BatchMode yes\nStrictHostKeyChecking no" > /var/lib/backuppc/.ssh/config
ssh-keygen -q -t rsa -b 4096 -N '' -C "BackupPC key" -f /var/lib/backuppc/.ssh/id_rsa
chmod 600 /var/lib/backuppc/.ssh/id_rsa
chmod 644 /var/lib/backuppc/.ssh/id_rsa.pub
chown -R backuppc-server:backuppc-server /var/lib/backuppc/.ssh
```

Check and download the lastest released versions:
* https://github.com/backuppc/backuppc-xs/releases/
* https://github.com/backuppc/rsync-bpc/releases/
* https://github.com/backuppc/backuppc/releases/
```shell
/usr/local/bin/rsync_bpc --version
perl -e 'use lib "/usr/local/BackupPC/lib"; use BackupPC::XS; print $BackupPC::XS::VERSION'
# Search for string like "# Version 4.3.0, released 25 Nov 2018." in /usr/local/BackupPC/bin/BackupPC

mkdir -p sources
cd sources

release_data=$(curl -s https://api.github.com/repos/backuppc/backuppc-xs/releases/latest)
backuppc_xs_ver=$(echo ${release_data} | jq -r ".tag_name")
backuppc_xs_tar=$(echo ${release_data} | jq -r ".assets[0].name")
wget $(echo ${release_data} | jq -r ".assets[0].browser_download_url")
tar -xzvf ${backuppc_xs_tar}
cd BackupPC-XS-${backuppc_xs_ver}

wget https://github.com/backuppc/backuppc-xs/releases/download/0.57/BackupPC-XS-0.57.tar.gz
wget https://github.com/backuppc/rsync-bpc/releases/download/3.0.9.12/rsync-bpc-3.0.9.12.tar.gz
wget https://github.com/backuppc/backuppc/releases/download/4.2.1/BackupPC-4.2.1.tar.gz
tar -xzvf BackupPC-XS-0.57.tar.gz
tar -xzvf rsync-bpc-3.0.9.12.tar.gz
tar -xzvf BackupPC-4.2.1.tar.gz
```
Install dependencies
```shell
cd BackupPC-XS-0.57/
perl Makefile.PL
make
make test
make install

cd ../rsync-bpc-3.0.9.12/
./configure
make
make install
```
Install BackupPC
```shell
cd ../BackupPC-4.2.1/
# [!] When installing, use this. Change '--hostname backuppc' to the actual host name
./configure.pl --batch --cgi-dir /var/www/cgi-bin/BackupPC --data-dir /var/lib/backuppc \
  --hostname $(hostname -f) --html-dir /var/www/html/BackupPC --html-dir-url /BackupPC \
  --install-dir /usr/local/BackupPC --backuppc-user=backuppc-server

# When upgrading, use this instead:
service backuppc stop
./configure.pl --batch --config-path /etc/BackupPC/config.pl
service backuppc start
```
Only for new installation, skip this for upgrade
```shell
# The following is good also when upgrading, unless the file contains custom modifications.
# Allows to connect to web UI from anywhere, not only from 127.0.0.1 by removing the following lines:
# order deny,allow
# deny from all
# allow from 127.0.0.1
cp httpd/BackupPC.conf /etc/apache2/conf-available/backuppc.conf
#sed -i "/deny\ from\ all/d" /etc/apache2/conf-available/backuppc.conf
#sed -i "/deny\,allow/d" /etc/apache2/conf-available/backuppc.conf
#sed -i "/allow\ from/d" /etc/apache2/conf-available/backuppc.conf
# Actually it's better to replace 'allow from 127.0.0.1' with something
# like 'allow from 127.0.0.1 192.168.0.1/24' or 'allow from all'

cp /etc/apache2/envvars{,.bak}
# Note that changing the apache user and group (next two commands) could cause other services
# provided by apache to fail. There are alternatives if you don't want to change the apache
# user: use SCGI or a setuid BackupPC_Admin script - see the docs.
sed -i "s/export APACHE_RUN_USER=www-data/export APACHE_RUN_USER=backuppc-server/" /etc/apache2/envvars
sed -i "s/export APACHE_RUN_GROUP=www-data/export APACHE_RUN_GROUP=backuppc-server/" /etc/apache2/envvars

cp /var/www/html/index.html{,.bak}
echo '<html><head><meta http-equiv="refresh" content="0; url=/BackupPC_Admin"></head></html>' > /var/www/html/index.html

a2enconf backuppc
a2enmod cgid
service apache2 restart

cp systemd/backuppc.service /etc/systemd/system
sed -i "s/#Group=backuppc/Group=backuppc/" /etc/systemd/system/backuppc.service
systemctl daemon-reload
systemctl enable backuppc.service

chmod u-s /var/www/cgi-bin/BackupPC/BackupPC_Admin

touch /etc/BackupPC/BackupPC.users

cp /etc/BackupPC/config.pl{,.bak}
nano /etc/BackupPC/config.pl
# Replace
#    $Conf{CgiAdminUserGroup} = '';
#    $Conf{CgiAdminUsers}     = '';
# with
#    $Conf{CgiAdminUserGroup} = 'backuppc';
#    $Conf{CgiAdminUsers} = 'backuppc';
# Actually we need only CgiAdminUsers, do we?

chown -R backuppc-server:backuppc-server /etc/BackupPC

htpasswd /etc/BackupPC/BackupPC.users backuppc

service backuppc start

# Configure mail delivery
# Add alias for backuppc user
nano /etc/aliases
newaliases
# Or change in 'Edit Config' > 'Email' > 'EMailAdminUserName' ($Conf{EMailAdminUserName} in /etc/BackupPC/config.pl)
```

### Maintenance
```shell
# View zlib-compressed log file
printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - XferLOG.5.z | gzip -dc | less
# or use BackupPC_zcat - as backuppc server (!) user
/usr/local/BackupPC/bin/BackupPC_zcat /var/lib/backuppc/pc/hostname/XferLOG.1.z

# List backup contents
/usr/local/BackupPC/bin/BackupPC_ls -h hostname -n 26 -s /home /

# Check email delivery
# [!] as user backuppc
/usr/local/BackupPC/bin/BackupPC_sendEmail -u user[@domain.tld]
# or stop backuppc service and then run
/usr/local/BackupPC/bin/BackupPC_sendEmail -c
# It will check if BackupPC is running, and should send an email to $Conf{EMailAdminUserName} if it is not
# [!] Don't forget to start backuppc service back

# -R - recursive, -i - view inode
/usr/local/BackupPC/bin/BackupPC_ls [-iR] [-h host] [-n bkupNum] [-s shareName] dirs/files... 
# example
/usr/local/BackupPC/bin/BackupPC_ls -h win-server -n 6 -s /mnt/smb/win-server/share dir1/dir2

# delete an entire backup, or a directory path within a backup
/usr/local/BackupPC/bin/BackupPC_backupDelete

# [!] Use screen utility
# Use quotes for path with spaces
./BackupPC_backupDelete -h host_name -n 4 -s Backup-Data-Folder "/path/with a space"
```
* Re: [BackupPC-users] delete backup: https://sourceforge.net/p/backuppc/mailman/message/35851832/
* Delete files from Backups: https://sourceforge.net/p/backuppc/mailman/message/36287909/

### Client config
```
visudo -f /etc/sudoers.d/backuppc
```
`/etc/sudoers.d/backuppc` content
```
# Allow backuppc to read files with rsync over SSH
backuppc ALL=NOPASSWD: /usr/bin/rsync
```
